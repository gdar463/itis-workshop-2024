# storage

Requires [bun](https://bun.sh) and [postgresql](https://postgresql.org)

To install:

```bash
bun i
createdb file_storage
psql file_storage
```

in psql

```sql
CREATE USER filestorage WITH CREATEDB ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE file_storage TO filestorage;
GRANT ALL ON SCHEMA public TO filestorage;
```

and in the .env file change the DATABASE_URL entry to

```markdown
"postgresql://filestorage:<password>@localhost:5432/file_storage?schema=public"
```

in this dir

```bash
bunx prisma migrate dev init
```
