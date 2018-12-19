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
### Requirements
* Python version 3.6+
* pip3

### Running
`./acrobat [options]`
