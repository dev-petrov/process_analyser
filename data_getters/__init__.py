import psutil as ps
import pandas as pd
import threading
from datetime import datetime

class BaseGetter:
    def get_data(self, *args, **kwargs):
        raise NotImplementedError()

class ProcessGetter(BaseGetter):
    def __init__(self, filter_processes=[], exclude_processes=[]):
        self.filter_processes = filter_processes
        self.exclude_processes = exclude_processes
        self.current_pid = threading.current_thread().native_id
    
    def _enrich_process(self, process):
        process = process.info
        process['open_files'] = len(process['open_files']) if process['open_files'] else 0
        process['connections'] = len(process['connections']) if process['connections'] else 0
        process['cmdline'] = ' '.join(process['cmdline']) if process['cmdline'] else None
        process['dttm'] = self.dttm
        try:
            parent_name = ps.Process(process['ppid']).name()
        except:
            parent_name = None
        process['parent_name'] = parent_name

        return process

    def get_data(self):
        self.dttm = datetime.now().timestamp()
        
        def _filter_process(process):
            process = process.info
            if process['pid'] == self.current_pid or process['name'] in self.exclude_processes\
                or (self.filter_processes and not (process['name'] in self.filter_processes)):
                return False
            
            return True

        processes = list(
            map(
                self._enrich_process,
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

        return pd.to_datetime(self.dttm, unit='s'), pd.DataFrame(
            data=processes, 
            columns=[
                'dttm', 'pid', 'name', 'username', 'ppid', 'parent_name',
                'cpu_percent', 'memory_percent', 'num_threads', 'terminal',
                'nice', 'cmdline', 'exe', 'status', 'create_time', 
                'connections', 'open_files'
            ]
        )

    def __str__(self):
        return "ProcessGetter"
