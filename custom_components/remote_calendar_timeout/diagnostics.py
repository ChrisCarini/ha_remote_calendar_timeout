"""Provides diagnostics for the remote calendar."""

import datetime
from typing import Any

from ical.diagnostics import redact_ics
from httpx import ReadTimeout

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from . import RemoteCalendarConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: RemoteCalendarConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    payload: dict[str, Any] = {
        "now": dt_util.now().isoformat(),
        "timezone": str(dt_util.get_default_time_zone()),
        "system_timezone": str(datetime.datetime.now().astimezone().tzinfo),
    }
    payload["ics"] = "\n".join(redact_ics(coordinator.ics))
    return payload

def get_timeout(err: ReadTimeout) -> str:
    return err._request.extensions.get('timeout', {'connect':'No timeout set'}).get('connect', 'No timeout set')