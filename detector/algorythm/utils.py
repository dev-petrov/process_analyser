from decimal import Decimal

import numpy as np

from .splits import SplitsCollection
from .states import StatesCollection


def json_default(obj):  # pragma: no cover
    if isinstance(obj, Decimal):
        return str(obj)
    elif isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, tuple):
        return list(obj)
    elif isinstance(obj, np.int64):
        return int(obj)
    elif isinstance(obj, (SplitsCollection, StatesCollection)):
        return obj.to_dict()
    return str(obj)
