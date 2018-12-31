# Acrobat v1.0.0
🦑 Acrobat - Quick query analysis
```
usage: acrobat [-h] [--dir DIR] [--setup SETUP] [--teardown TEARDOWN]
               [--schema SCHEMA]
               {analyze,a,list,ls} ...

Quick PERFORMance analyzer, acrobats perform, get it?

positional arguments:
  {analyze,a,list,ls}
    analyze (a)        Analyze all sql queries in sql dir
    list (ls)          List all available queries

optional arguments:
  -h, --help           show this help message and exit
  --dir DIR            Override sql directory, default sql/
  --setup SETUP        Override setup sql file, default make_tables.sql
  --teardown TEARDOWN  Override teardown sql file, default drop_tables.sql
  --schema SCHEMA      Override schema sql file, default make_schema.sql
```


## Usage
### How it works
Make a SQL directory, put SQL in it, watch it run. This tool makes the following assumptions:
- Make tables with `make_tables.sql`
- Drop tables with `drop_tables.sql`
- Make the custom schema (because you wouldn't speed test in prod, right?) with `make_schema.sql`

You can change any of these files with the options listed above.
### Requirements
* Python version 3.6+
* pip3

### Running
```
cd /path/to/acrobat/
virtualenv -p `which python3` venv
source venv/bin/activate
pip install -r requirements.txt
```
`./acrobat [options]`
