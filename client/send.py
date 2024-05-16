import os
import time
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
        ip = parent.parent().ip
        file = open(filename[0], "r")
        magicMime = magic.Magic(mime=True)
        mime = magicMime.from_file(filename[0])
        try: 
            request = requests.post(ip + "/upload?name=" +  urllib.parse.quote_plus(filename[0].split("/")[-1]), file, headers={
                "Content-Type": mime
                })
        except Exception:
            parent.spinner.stop()
            _ = Dialog("Errore", "<p style=\"font-size:13px\">Il server non ha risposto alla richiesta.<br />Riprovare più tardi</p>").exec()
            return
        match request.status_code:
            case 200:
                secret: dict[str, str] = request.json()
                if not os.path.isfile("recent.txt"):
                    _ = open("recent.txt", "xt")
                with open("recent.txt", "at") as f:
                    _ = f.write(filename[0].split("/")[-1].replace(";", ",") + ";" + secret["code"] + ";" + str(time.time()) + "\n")
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
        ip = parent.parent().ip
        try:
            request = requests.get(ip + "/download?secret=" + urllib.parse.quote_plus(password), headers={
                "Accept": "*"
                })
        except Exception:
            parent.spinner.stop()
            _ = Dialog("Errore", "<p style=\"font-size:13px\">Il server non ha risposto alla richiesta.<br />Riprovare più tardi</p>").exec()
            return False
        match request.status_code:
            case 200:
                filename = request.headers["X-File-Name"]
                with open("recent.txt", "w+t") as f:
                    saved: list[str] = f.readlines()
                    secrets = []
                    for i in range(len(saved)):
                        secrets.append(saved[i].split(";")[1])
                    index = secrets.index(password)
                    _ = saved.pop(index)
                    f.writelines(saved)
                QFileDialog.saveFileContent(request.content, filename)
                parent.spinner.stop()
                # _ = Dialog("Successo", "<p style=\"font-size:13px\">Ricevuto il file con successo.</p>").exec()
                return True
            case 404:
                parent.spinner.stop()
                _ = Dialog("Errore", "<p style=\"font-size:13px\">Non esiste un file associato alla password.<br />Controlla che la password sia giusta o che non sia già stato scaricato il file.</p>").exec()
                return False
            case _:
                parent.spinner.stop()
                _ = Dialog("Errore", "<p style=\"font-size:13px\">Il server ha risposto con il codice " + str(request.status_code) +
                                " e il corpo:<br /><br />" + request.text + "<br /><br />Riprova più tardi </p>").exec()
                return False
    else:
        parent.spinner.stop()
        _ = Dialog("Messaggio", "<p style=\"font-size:13px\">Non hai immesso nessuna password</p>").exec()
        return False

