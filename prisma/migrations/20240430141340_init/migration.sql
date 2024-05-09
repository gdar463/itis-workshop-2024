-- CreateTable
CREATE TABLE "File" (
    "id" SERIAL NOT NULL,
    "secretWord" TEXT NOT NULL,
    "fileName" TEXT NOT NULL,
    "discordId" TEXT NOT NULL,

    CONSTRAINT "File_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "File_secretWord_key" ON "File"("secretWord");

-- CreateIndex
CREATE UNIQUE INDEX "File_discordId_key" ON "File"("discordId");
