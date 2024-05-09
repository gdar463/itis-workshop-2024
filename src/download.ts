import type { TextChannel } from "discord.js";
import { client } from ".";
import { config } from "./config";
import prisma from "./db";
import chalk from "chalk";
import { consolelog } from "./util";

export async function download(url: URL) {
    consolelog(chalk.blueBright("Richiesto file"));
    consolelog(
        `${chalk.cyanBright("URL:")} ${chalk.greenBright(url.toString())}`,
    );
    const params = url.searchParams;
    if (!params.has("secret")) {
        consolelog(chalk.redBright("ERRORE: Nessuna password nella richiesta"));
        return new Response("Missing secret param", { status: 400 });
    }

    const fromDB = await prisma.file.findUnique({
        where: {
            secretWord: params.get("secret")!,
        },
        select: {
            discordId: true,
        },
    });

    if (fromDB === null || fromDB === undefined) {
        consolelog(
            chalk.redBright("ERRORE: Nessun file assocciato alla passoword"),
        );
        return new Response(
            "A file corrisponding to the secret doesn't exist",
            { status: 404 },
        );
    }

    consolelog(`${chalk.cyanBright("Trovato il messaggio con id:")} ${chalk.greenBright(fromDB.discordId)}`)

    const channel = (await (
        await client.channels.fetch(config.DISCORD_CHANNEL_ID)
    )?.fetch()) as TextChannel;

    const message = await channel.messages.fetch(fromDB?.discordId!);
    const attachment = message.attachments.at(0)!;
    consolelog(`${chalk.cyanBright("Trovato il file con nome:")} ${chalk.greenBright(attachment.name)}`)

    const contentType = attachment.contentType!;
    const file = await (await fetch(attachment.url)).blob();
    consolelog(chalk.cyanBright("Ottenuto il blob del file"))

    await prisma.file.delete({
        where: {
            secretWord: params.get("secret")!,
        },
    });
    consolelog(chalk.cyanBright("Cancellato dal database il file"))
    
    await message.delete();

    consolelog(chalk.redBright("Inviando file a client...\n\n"))
    return new Response(file, {
        headers: {
            "X-File-Name": attachment.name,
            "Content-Type": contentType,
        },
    });
}
