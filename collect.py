import time as systime
import argparse
from random import randint

from utils import get_instance

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data collector')
    parser.add_argument('--collector', help='Type of collector', default='csv', choices=['csv', 'db'])
    parser.add_argument('--filename', help='File name for csv collector', type=str)
    parser.add_argument('--min_interval', help='Min interval in secs for trigger collect, no effect when use_rand=false', default=1, type=int)
    parser.add_argument('--max_interval', help='Max interval in secs for trigger collect, no effect when use_rand=false', default=300, type=int)
    parser.add_argument('--use_rand', help='User random interval', default=True, type=bool)
    parser.add_argument('--interval', help='Interval in secs for trigger collect, no effect when use_rand=true', default=60, type=int)



    args = parser.parse_args()

    collector = get_instance('collector', args, instance_kwargs={'verbose': True})

    print("Starting collector service.")
    print(f"Using collector: {collector}")
    use_rand = args.use_rand
    min_interval = args.min_interval
    max_interval = args.max_interval
    interval = args.interval

    if use_rand:
        print(f"Using random interval from {min_interval} to {max_interval} secs")
    else:
        print(f"Using interval {interval} secs")

    print("Collecting...")

    while True:
        collector.collect()
        interval = args.interval
        if use_rand:
            interval = randint(min_interval, max_interval)
        print(f"Sleeping {interval} secs...")
        systime.sleep(interval)
