import dotenv from "dotenv";

let PASSWORD_TYPE;
if (process.env.PASSWORD_TYPE) {
    PASSWORD_TYPE = process.env.PASSWORD_TYPE;
}

let DEBUG;
if (process.env.DEBUG) {
    DEBUG = process.env.DEBUG;
}

dotenv.config();

const { DISCORD_TOKEN, DISCORD_CLIENT_ID, DISCORD_CHANNEL_ID } = process.env;

if (!DISCORD_TOKEN) {
    throw new Error("Missing token");
}
if (!DISCORD_CLIENT_ID) {
    throw new Error("Missing client id");
}
if (!DISCORD_CHANNEL_ID) {
    throw new Error("Missing channel id");
}

if (process.env.PASSWORD_TYPE && !PASSWORD_TYPE) {
    PASSWORD_TYPE = process.env.PASSWORD_TYPE;
} else if (!PASSWORD_TYPE) {
    PASSWORD_TYPE = "0";
}

if (process.env.DEBUG && !DEBUG) {
    DEBUG = process.env.DEBUG;
} else if (!DEBUG) {
    DEBUG = "";
}

// const USER_AGENT = "File Storage ( github.com/gdar463, 0.1.0 )";
// const BASE_URL = "https://discord.com/api/v10";
// const AUTH = `Bot ${DISCORD_TOKEN}`;

export const config = {
    DISCORD_TOKEN,
    DISCORD_CLIENT_ID,
    DISCORD_CHANNEL_ID,
    PASSWORD_TYPE,
    DEBUG,
    // USER_AGENT,
    // BASE_URL,
    // AUTH,
};
