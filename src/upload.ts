import type { TextChannel } from "discord.js";
import { client } from ".";
import { config } from "./config";
import { tmpNameSync } from "tmp";
import prisma from "./db";
import { generate, consolelog } from "./util";
import chalk from "chalk";
import { readableStreamToArrayBuffer } from "bun";

export async function upload(
    url: URL,
    headers: Headers,
    blob: ReadableStream<Uint8Array> | null,
) {
    consolelog(chalk.blueBright("Ricevuto file"));
    consolelog(
        `${chalk.cyanBright("URL:")} ${chalk.greenBright(url.toString())}`,
    );
    consolelog(
        `${chalk.cyanBright("Content-Type:")} ${chalk.greenBright(headers.get("Content-Type"))}`,
    );
    const params = url.searchParams;
    if (!params.has("name")) {
        return new Response("Missing name param", { status: 400 });
    }

    if (blob === null) {
        return new Response("Missing file", { status: 400 });
    }

    let secret;
    switch (config.PASSWORD_TYPE) {
        case "1":
            secret = generate(16);
            break;
        case "2":
            secret = Buffer.from(
                Array.from(crypto.getRandomValues(new Int8Array(32))).join(""),
            ).toString("base64");
            break;
        default:
            secret = generate(6);
            break;
    }
    consolelog(
        `${chalk.cyanBright("Generato segreto:")} ${chalk.greenBright(secret)}`,
    );

    const path = tmpNameSync();
    consolelog(
        `${chalk.cyanBright("Temp path a:")} ${chalk.greenBright(path)}`,
    );

    await Bun.write(path, await readableStreamToArrayBuffer(blob));
    consolelog(
        `${chalk.cyanBright("Scritto file a:")} ${chalk.greenBright(path)}`,
    );

    let message;
    try {
        const channel = (await (
            await client.channels.fetch(config.DISCORD_CHANNEL_ID)
        )?.fetch()) as TextChannel;
        message = await channel.send({
            files: [
                {
                    attachment: path,
                    name: params.get("name")!,
                    description: "magical file",
                },
            ],
        });
    } catch (e) {
        return new Response("Failed to send message", { status: 500 });
    }
    consolelog(
        `${chalk.cyanBright("Inviato file a canale con id:")} ${chalk.greenBright(message.id)}`,
    );

    try {
        await prisma.file.create({
            data: {
                fileName: params.get("name")!,
                secretWord: secret,
                discordId: message.id,
            },
        });
    } catch (e) {
        return new Response("Failed to access database");
    }
    consolelog(chalk.cyanBright("Mandato a database informazioni"));

    consolelog(chalk.redBright("Inviando risposta a client...\n\n"));
    return new Response(`{"code":"${secret}"}`, {
        status: 200,
        headers: { "Content-Type": "application/json" },
    });
}
