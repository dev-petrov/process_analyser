[![codecov](https://codecov.io/gh/dev-petrov/process_analyser/branch/master/graph/badge.svg?token=CQM9I7ASTH)](https://codecov.io/gh/dev-petrov/process_analyser)
[![CI](https://github.com/dev-petrov/process_analyser/workflows/CI/badge.svg)](https://github.com/dev-petrov/process_analyser/actions/workflows/ci-tests.yml)

# Детектор аномальных состояний сервера

- [Детектор аномальных состояний сервера](#детектор-аномальных-состояний-сервера)
  - [Описание компонентов](#описание-компонентов)
    - [aggregators](#aggregators)
    - [algorythms](#algorythms)
    - [collectors](#collectors)
    - [data_getters](#data_getters)
    - [db](#db)
    - [loggers](#loggers)
    - [main.py](#mainpy)
  - [Команды](#команды)
    - [collect](#collect)
      - [Описание](#описание)
      - [Использование](#использование)
      - [Параметры](#параметры)
    - [detect](#detect)
      - [Описание](#описание-1)
      - [Использование](#использование-1)
      - [Параметры](#параметры-1)
    - [import](#import)
      - [Описание](#описание-2)
      - [Использование](#использование-2)
      - [Параметры](#параметры-2)
    - [shell](#shell)
      - [Описание](#описание-3)
      - [Использование](#использование-3)

## Описание компонентов

### aggregators
Содержит класс агрегации данных.

### algorythms
Содержит класс алгоритма детектирования аномалий.

### collectors
Cодержит классы сбора данных.

На данный моменты доступны следующие:
- csv - класс для сбора данных в csv файл
- db - класс для сбора данных в базу данных

### data_getters
Содержит класс для получения данных через [psutil](https://psutil.readthedocs.io).

### db
Модуль базы данных.

### loggers
Содержит классы логеров.

На данный моменты доступны следующие:
- console - класс для логирования в консоль
- db - класс для логирования в базу данных
- file - класс для логирования в файл

### main.py

Скрипт для запуска [команд](#команды)

## Команды

### collect

#### Описание

Запуск процесса сбора исторических данных.

#### Использование

```bash
python main.py collect --collector csv --filename data.csv
```

#### Параметры

- `--collector` - тип [сборщика данных](#collectors)
- `--filename` - название файла для csv сборщика

### detect

#### Описание

Запуск процесса детектирования аномалий.

#### Использование
```bash
python main.py detect --logger file --verbose true
```

#### Параметры

- `--logger` - тип [логера](#loggers)
- `--logger_filename` - название файла для файлового логера
- `--verbose` - выводить дополнительную информацию

### import

#### Описание

Импорт данных из csv в базу данных.

#### Использование

```bash
python main.py import --file_type csv --filename data.csv
```

#### Параметры

- `--file_type` - тип импортируемого файла (csv, xlsx)
- `--filename` - название файла из корого импортируем

### shell

#### Описание

Запускает IPython и конфигурирует подключение к базе данных.

#### Использование

```bash
python main.py shell
```
