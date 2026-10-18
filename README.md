# pg_export_bytea

![pg_export_bytea](pg_export_bytea.png)

A CLI helping tool for exporting bytea fields of a PostgreSQL relation into files

## Usage

```
Description:
  A CLI helping tool for exporting bytea fields of a PostgreSQL relation into files

Usage:
  export [options] [--] <sql>...

Arguments:
  sql                        SQL queries returning 'filename' and 'binary' columns

Options:
      --host[=HOST]          database server host or socket directory (default: "local socket") [default: "/var/run/postgresql/"]
  -u, --username[=USERNAME]  database user name [default: "cyprien.diot@local.groupepsih.com"]
  -d, --dbname[=DBNAME]      database name [default: "public"]
  -p, --port[=PORT]          database server port [default: 5432]
  -W, --prompt               prompt for password. Or use the POSTGRES_PASSWORD environment variables
  -o, --output[=OUTPUT]      output directory path [default: "/home/cyprien.diot@local.groupepsih.com/work/cyprien.diot/pg_export_bytea"]
  -h, --help                 Display help for the given command. When no command is given display help for the list command.
  -q, --quiet                Do not output any message.
  -V, --version              Display this application version.
      --ansi                 Force ANSI output.
      --no-ansi              Disable ANSI output.
  -n, --no-interaction       Do not ask any interactive question.
  -v|vv|vvv, --verbose       Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug.
```

## Exemple

### Start up a database
```
docker compose up
```
- It will import files from `docker/init/` directory into a `test` table

### Export files from database

```
mkdir tmp
pg_export_bytea export --host=localhost --username=postgres -W --dbname=postgres --output=tmp/ "SELECT filename, content as binary FROM test"
```

- Will read all rows from table "test" in database postgres on localhost
- It will use "postgres" user and prompt for password
- It will output files in the `tmp/` directory using filenames from the `filename` column and filecontent from the `content` column

## Download et and setup

Use poetry pip package with `poetry build`

## Testing

See Gitlab-CI file definition 

## Contributing

You'll need
- Python >= 3.8
- Poetry >= 1.4


```
poetry install
poetry shell

```
