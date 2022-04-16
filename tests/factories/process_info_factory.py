from dataclasses import dataclass
from datetime import datetime
from random import choice, randint, uniform

import factory


@dataclass
class ProcessInfo:
    dttm: datetime
    pid: int
    name: str
    username: str
    ppid: int
    parent_name: str
    cpu_percent: float
    memory_percent: float
    num_threads: int
    terminal: str
    nice: int
    cmdline: str
    exe: str
    status: str
    create_time: datetime
    connections: int
    open_files: int


class ProcessInfoFactory(factory.Factory):

    dttm = factory.LazyFunction(datetime.now)
    pid = factory.LazyFunction(lambda: randint(1, 1000))
    name = factory.Faker("name")
    username = factory.Faker("name")
    ppid = factory.LazyFunction(lambda: randint(1, 1000))
    parent_name = factory.Faker("name")
    cpu_percent = factory.LazyFunction(lambda: uniform(0, 100))
    memory_percent = factory.LazyFunction(lambda: uniform(0, 100))
    num_threads = factory.LazyFunction(lambda: randint(0, 10))
    terminal = factory.Faker("file_path")
    nice = factory.LazyFunction(lambda: randint(-20, 20))
    cmdline = factory.Faker("file_path")
    exe = factory.Faker("file_path")
    status = factory.LazyFunction(lambda: choice(["running", "idle", "sleeping"]))
    create_time = factory.LazyFunction(datetime.now)
    connections = factory.LazyFunction(lambda: randint(0, 10))
    open_files = factory.LazyFunction(lambda: randint(0, 10))

    class Meta:
        model = ProcessInfo
