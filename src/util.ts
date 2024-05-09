import { config } from "./config";

export function generate(n: number): string {
    var add = 1,
        max = 12 - add;
    if (n > max) {
        return generate(max) + generate(n - max);
    }

    max = Math.pow(10, n + add);
    var min = max / 10;
    var number = Math.floor(Math.random() * (max - min + 1)) + min;

    return ("" + number).substring(add);
}

// @ts-expect-error
async function streamToBuffer(readableStream) {
    return new Promise((resolve, reject) => {
        const chunks: Array<Buffer> = [];
        readableStream.on("data", (data: any) => {
            if (typeof data === "string") {
                // Convert string to Buffer assuming UTF-8 encoding
                chunks.push(Buffer.from(data, "utf-8"));
            } else if (data instanceof Buffer) {
                chunks.push(data);
            } else {
                // Convert other data types to JSON and then to a Buffer
                const jsonData = JSON.stringify(data);
                chunks.push(Buffer.from(jsonData, "utf-8"));
            }
        });
        readableStream.on("end", () => {
            resolve(Buffer.concat(chunks));
        });
        readableStream.on("error", reject);
    });
}

export function consolelog(str: string) {
    if (config.DEBUG === "Y" || config.DEBUG === "S") {
        console.log(str);
    }
}
