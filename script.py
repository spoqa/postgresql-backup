#!/usr/bin/env python3
import argparse
import datetime
import subprocess
from pathlib import Path, PurePath


parser = argparse.ArgumentParser()
parser.add_argument('database_url', metavar='DATABASE_URL', type=str)
parser.add_argument('s3_path', metavar='BUCKET:PREFIX', type=str)
parser.add_argument('--postfix', type=str, default='dump')

if __name__ == '__main__':
    args = parser.parse_args()
    bucket, prefix, *_rest = args.s3_path.split(':', 1) + [None]
    postfix = args.postfix
    filename = '{}.{}'.format(datetime.date.today().isoformat(), postfix)
    filepath = Path('/out') / filename
    subprocess.check_call(
        [
            'pg_dump', '--format=c', '-v',
            '-f', str(filepath),
            args.database_url,
        ]
    )
    s3_key = PurePath('/') / prefix / filename.replace('-', '/', 1)
    s3_uri = 's3://' + bucket + str(s3_key)
    subprocess.check_call(
        [
            'aws', 's3', 'cp',
            str(filepath), s3_uri,
        ]
    )
