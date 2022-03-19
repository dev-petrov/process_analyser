import argparse
import pandas as pd
from sqlalchemy.orm import Session
from db import RawValue, engine

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import data helper')
    parser.add_argument('--file_type', help='Type of file', default='csv', choices=['csv', 'xlsx'])
    parser.add_argument('--filename', help='File name', type=str, required=True)

    args = parser.parse_args()

    readers = {
        'csv': pd.read_csv,
        'xlsx': pd.read_excel,
    }

    print(f'Reading {args.file_type} file...')

    df = readers[args.file_type](
        args.filename, 
        names=[
            'dttm', 'pid', 'name', 'username', 'ppid', 'parent_name',
            'cpu_percent', 'memory_percent', 'num_threads', 'terminal',
            'nice', 'cmdline', 'exe', 'status', 'create_time', 
            'connections', 'open_files'
        ]
    )

    print('Importing...')

    with Session(engine) as session, session.begin():
        # TODO check for duplicates
        df.dttm = pd.to_datetime(df.dttm, unit='s')
        df.create_time = pd.to_datetime(df.create_time, unit='s')
        session.add_all(
            [
                RawValue(**kwargs)
                for kwargs in df.to_dict('records')
            ]
        )

    print(f'Successfully imported {len(df)} rows.')
