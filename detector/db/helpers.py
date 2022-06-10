from sqlalchemy import Time, cast, create_engine, func, literal_column

from detector.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_PREFIX, DB_USER


def get_engine(
    test=False, host=DB_HOST, name=DB_NAME, password=DB_PASSWORD, port=DB_PORT, prefix=DB_PREFIX, user=DB_USER
):  # pragma: no cover
    db_url = None
    name = f"{name}_test" if test else name
    if "sqlite" in prefix:
        if test:
            name = ""
        db_url = "{}://{}".format(
            prefix,
            name,
        )
    else:
        db_url = "{}://{}:{}@{}:{}/{}".format(
            prefix,
            user,
            password,
            host,
            port,
            name,
        )
    return create_engine(db_url)


def extract_time(expr, db_prefix=DB_PREFIX):  # pragma: no cover
    if "sqlite" in db_prefix:
        return func.TIME(expr)

    return cast(expr, Time)


def string_agg(expr, sep=",", db_prefix=DB_PREFIX):  # pragma: no cover
    if "sqlite" in db_prefix:
        return func.group_concat(expr, literal_column(f"'{sep}'"))

    return func.string_agg(expr, literal_column(f"'{sep}'"))
