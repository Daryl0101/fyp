# region System
from app_backend.enums import Interval


SUCCESS_DICT = {"status_name": "Success", "errors": None, "model": None}
FAILED_DICT = {"status_name": "Failed", "errors": None, "model": None}
# endregion

# region Dashboard
PERIOD = {
    Interval.DAY: 0,
    Interval.WEEK: 7,
    Interval.MONTH: 30,
    Interval.YEAR: 365,
}

# endregion
