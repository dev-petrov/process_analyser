from datetime import datetime, timedelta
import time as systime
import argparse
from db import RawCleanedValue

from utils import get_instance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data collector')
    parser.add_argument('--collector', help='Type of collector', default='csv', choices=['csv', 'db'])
    parser.add_argument('--filename', help='File name for csv collector', type=str)

    args = parser.parse_args()

    args.raw_values_cls = RawCleanedValue

    collector = get_instance('collector', args, instance_kwargs={'verbose': True})

    print("Starting collector service.")
    print(f"Using collector: {collector}")

    print("Collecting...")

    while True:
        next_run_at = datetime.now() + timedelta(seconds=60)
        collector.collect()
        sleep_secs = (next_run_at - datetime.now()).total_seconds()
        print(f"Sleeping {sleep_secs} secs...")
        systime.sleep(sleep_secs)
