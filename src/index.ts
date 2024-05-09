import { config } from "./config";
import { download } from "./download";
import { upload } from "./upload";
import chalk from "chalk";
import { Client } from "discord.js";

const server = Bun.serve({
    async fetch(req) {
        const url = new URL(req.url);
        const path = url.pathname;
        const method = req.method;

        console.log(chalk.magentaBright(`Colpito ${path}`));

        try {
            if (path === "/upload" && method === "POST") {
                const headers = req.headers;
                const blob = req.body;
                return await upload(url, headers, blob);
            } else if (path === "/download" && method === "GET") {
                return await download(url);
            }
        } catch {
            console.log(chalk.redBright("Errore"));
            return new Response("Server Error", { status: 500 });
        }

        return new Response("Not Found", { status: 404 });
    },

    port: process.env.PORT || 8080,
});

export const client = new Client({ intents: ["MessageContent"] });

client.on("ready", () => {
    console.log("Bot pronto\n");
});

client.login(config.DISCORD_TOKEN);

console.log(`Ascoltando su porta ${server.port}`);
