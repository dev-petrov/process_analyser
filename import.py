import argparse
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from db import RawCleanedValue, engine

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

    with Session(engine) as session:
        # TODO check for duplicates
        df.dttm = pd.to_datetime(df.dttm, unit='s')
        df.create_time = pd.to_datetime(df.create_time, unit='s')
        total_rows = len(df)
        chunks = np.array_split(df.to_dict('records'), int(total_rows / 10000) + 1)
        del df
        added_rows = 0
        for chunk in chunks:
            with session.begin():
                session.add_all(
                    [
                        RawCleanedValue(**kwargs)
                        for kwargs in chunk
                    ]
                )
                added_rows += len(chunk)
                print(f"Added {round((added_rows / total_rows) * 100, 2)}% rows.")

    print(f'Successfully imported {total_rows} rows.')
