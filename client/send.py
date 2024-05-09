import urllib.parse
from PyQt6.QtCore import pyqtSlot 
from PyQt6.QtWidgets import QFileDialog
import magic
import requests

from dialog import Dialog


@pyqtSlot()
def open_file_dialog(parent):
    parent.spinner.start()
    filename = QFileDialog.getOpenFileName(parent, "Apri file", "", "All Files (*)",)
    if filename[0] != "":
        ip = parent.ip_edit.text()
        file = open(filename[0], "r")
        mime = magic.Magic(mime=True)
        try: 
            request = requests.post(ip + "/upload?name=" +  urllib.parse.quote_plus(filename[0].split("/")[-1]), file, headers={
                "Content-Type": mime.from_file(filename[0])
                })
        except Exception:
            parent.spinner.stop()
            _ = Dialog("Errore", "<p style=\"font-size:13px\">Il server non ha risposto alla richiesta.<br />Riprovare più tardi</p>").exec()
            return
        match request.status_code:
            case 200:
                secret: dict[str, str] = request.json()
                parent.spinner.stop()
                _ = Dialog("Successo", "<p style=\"font-size:13px\">Inviato il file con successo. <br />Il codice del file è: " +
                                secret["code"] + "<br />Non perderlo, se no il file verrà perso per sempre</p>").exec()
                return
            case _:
                parent.spinner.stop()
                _ = Dialog("Errore", "<p style=\"font-size:13px\">Il server ha risposto con il codice " + str(request.status_code) +
                                " e il corpo:<br /><br />" + request.text + "<br /><br />Riprova più tardi </p>").exec()
                return
    else:
        parent.spinner.stop()
        _ = Dialog("Messaggio", "<p style=\"font-size:13px\">Non hai selezionato alcun file</p>").exec()

def get_file_from_server(parent):
    parent.spinner.start()
    password = parent.pass_edit.text()
    if password != "":
        ip = parent.ip_edit.text()
        try:
            request = requests.get(ip + "/download?secret=" + urllib.parse.quote_plus(password), headers={
                "Accept": "*"
                })
        except Exception:
            parent.spinner.stop()
            _ = Dialog("Errore", "<p style=\"font-size:13px\">Il server non ha risposto alla richiesta.<br />Riprovare più tardi</p>").exec()
            return
        match request.status_code:
            case 200:
                filename = request.headers["X-File-Name"]
                QFileDialog.saveFileContent(request.content, filename)
                parent.spinner.stop()
                _ = Dialog("Successo", "<p style=\"font-size:13px\">Ricevuto il file con successo.</p>").exec()
                return
            case 404:
                parent.spinner.stop()
                _ = Dialog("Errore", "<p style=\"font-size:13px\">Non esiste un file associato alla password.<br />Controlla che la password sia giusta o che non sia già stato scaricato il file.</p>").exec()
            case _:
                parent.spinner.stop()
                _ = Dialog("Errore", "<p style=\"font-size:13px\">Il server ha risposto con il codice " + str(request.status_code) +
                                " e il corpo:<br /><br />" + request.text + "<br /><br />Riprova più tardi </p>").exec()
                return
    else:
        parent.spinner.stop()
        _ = Dialog("Messaggio", "<p style=\"font-size:13px\">Non hai immesso nessuna password</p>").exec()

