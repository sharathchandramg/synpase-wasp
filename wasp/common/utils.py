import pendulum
from datetime import datetime
from typing import Any, Dict, Optional, Sequence, Union, cast
from wasp.config import settings

def date_or_today(date: Optional[Union[str, datetime.date]] = None) -> pendulum.Date:
    """Return parsed date, or current date in flow time zone.

    Args:
        date: An optional string in "YYYY-MM-DD" format or :py:class:`datetime.date`
            object.

    Returns:
        The parsed date from the provided string, or the provided date object, or the
        current date in the flow's time zone if date is not specified.
    """
    if not date:
        return pendulum.today(tz()).date()
    else:
        dt = cast(pendulum.DateTime, pendulum.parse(str(date)))
        return dt.date()

def tz() -> str:
    """Timezone string.

    Returns:
        The configured time zone, or "UTC" if not configured.
    """
    return settings.get("swarm.flows.timezone", "UTC")

def max_date() -> str:
    """maximum date

    Returns:
        Max date in configured in settings, else "9999-01-01"
    """
    return "9999-01-01"
