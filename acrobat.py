#!/usr/bin/env python3

import argparse
import os
import sys
import itertools
from pathlib import Path
import timeit
import psycopg2
from multiprocessing import Process
import time

SQL_DIR = Path.cwd() / 'sql'
SETUP_SQL = 'make_tables.sql'
TEARDOWN_SQL = 'drop_tables.sql'
SCHEMA_SQL = 'make_schema.sql'
CONNECTION = Path.cwd() / '.con'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description=('Quick PERFORMance analyzer,' +
                         + 'acrobats perform, get it?')
            )
    parser.add_argument(
            '--dir',
            type=Path,
            default='sql/',
            help='Override sql directory, default %(default)s'
            )
    parser.add_argument(
            '--setup',
            type=Path,
            default=SETUP_SQL,
            help='Override setup sql file, default %(default)s'
            )
    parser.add_argument(
            '--teardown',
            type=Path,
            default=TEARDOWN_SQL,
            help='Override teardown sql file, default %(default)s'
            )
    parser.add_argument(
            '--schema',
            type=Path,
            default=SCHEMA_SQL,
            help='Override schema sql file, default %(default)s'
            )
    subparsers = parser.add_subparsers(dest='cmd')

    analysis_parser = subparsers.add_parser(
        'analyze',
        aliases=['a'],
        help='Analyze all sql queries in sql dir'
        )
    analysis_parser.set_defaults(cmd=cmd_analyze)

    list_parser = subparsers.add_parser(
            'list',
            aliases=['ls'],
            help='List all available queries'
            )
    list_parser.set_defaults(cmd=cmd_list)

    return parser.parse_args()


def spinner(self, minutes=2):
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    end = time.time() + 60 * minutes
    while time.time() < end:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')


def setup(connection):
    try:
        print('Creating tables (this could take awhile)')
        conn = psycopg2.connect(connection)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(open(SQL_DIR / SCHEMA_SQL, 'r').read())
        cur.execute(open(SQL_DIR / SETUP_SQL, 'r').read())
        conn.commit()
        print('Tables loaded, moving on')
    except psycopg2.Error as e:
        print('PSQL error: {}'.format(e))
        if conn is not None:
            conn.close()
    except Exception as ee:
        print('Error: {}'.format(ee))


def cmd_analyze(args: argparse.Namespace) -> bool:
    connection = None
    files = [f for f in os.listdir(SQL_DIR)
             if f != 'make_tables.sql'
             and f != 'drop_tables.sql'
             and f != 'make_schema.sql']

    with open(CONNECTION) as con_file:
        connection = str(con_file.readline().replace('\n', ''))

    estimated_script_runtime = len(files) / 3
    setup_script = Process(target=setup, args=(connection,))
    spinner_script = Process(target=spinner, args=(estimated_script_runtime,))
    processes = [setup_script, spinner_script]
    for p in processes:
        p.start()

    print('Estimated time to completion: {} minutes'
          .format(estimated_script_runtime))
    try:
        conn = psycopg2.connect(connection)
        conn.autocommit = True
        cur = conn.cursor()
        for f in files:
            print('Running query for: {}'.format(f))
            start_time = timeit.default_timer()
            cur.execute(open(SQL_DIR / f).read())
            conn.commit()
            elapsed = timeit.default_timer() - start_time
            print('Query complete, time: {} seconds'.format(str(elapsed)))
            print('--------------------------------------')

        print('{} queries executed, cleaning'.format(len(files)))
        cur.execute(open(SQL_DIR / TEARDOWN_SQL, 'r').read())
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print('PSQL error: {}'.format(e))
        if conn is not None:
            conn.close()
    except Exception as ee:
        print('Error: {}'.format(ee))


def cmd_list(args: argparse.Namespace) -> bool:
    '''
    List all queries in the sql directory
    '''
    files = os.listdir(SQL_DIR)
    print('{} available SQL files to run:'.format(len(files)))
    for f in os.listdir(SQL_DIR):
        print(f)

    return True


def main():
    global SQL_DIR, SETUP_SQL, TEARDOWN_SQL, SCHEMA_SQL
    args = parse_args()

    if args.setup:
        SETUP_SQL = args.setup

    if args.teardown:
        TEARDOWN_SQL = args.teardown

    if args.dir:
        SQL_DIR = args.dir

    if args.schema:
        SCHEMA_SQL = args.schema

    if args.cmd is None:
        print('No option specified, use --help if you\'re stuck!')
        return False

    return args.cmd(args)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
