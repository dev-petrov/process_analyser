import psutil as ps
import pandas as pd
import threading
import time as systime
from sys import argv
from random import randint
from datetime import datetime

def get_processes(filter_processes=[], exclude_processes=[]):
    dttm = datetime.now().timestamp()
    current_pid = threading.current_thread().native_id

    def _enrich_process(process):
        process = process.info
        process['open_files'] = len(process['open_files']) if process['open_files'] else 0
        process['connections'] = len(process['connections']) if process['connections'] else 0
        process['cmdline'] = ' '.join(process['cmdline']) if process['cmdline'] else ''
        process['dttm'] = dttm
        process['parent_name'] = ps.Process(process['ppid']).name()

        return process
    
    def _filter_process(process):
        process = process.info
        if process['pid'] == current_pid or process['name'] in exclude_processes\
            or (filter_processes and not (process['name'] in filter_processes)):
            return False
        
        return True

    processes = list(
        map(
            _enrich_process,
            filter(
                _filter_process,
                ps.process_iter(
                    [
                        'pid', 'name', 'username', 'terminal', 
                        'num_threads', 'nice', 'exe', 'memory_percent',
                        'cmdline', 'create_time', 'connections', 'status',
                        'cpu_percent', 'ppid', 'open_files',
                    ]
                )
            )
        )
    )

    return pd.DataFrame(
        data=processes, 
        columns=[
            'dttm', 'pid', 'name', 'username', 'ppid', 'parent_name',
            'cpu_percent', 'memory_percent', 'num_threads', 'terminal',
            'nice', 'cmdline', 'exe', 'status', 'create_time', 
            'connections', 'open_files'
        ]
    )


def write_to_csv(filename):
    with open(filename, 'a') as file:
        file.write(get_processes().to_csv(header=False, index=False))

if __name__ == '__main__':
    filename = argv[1]

    while True:
        write_to_csv(filename)
        systime.sleep(randint(1, 1800))
