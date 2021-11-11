from typing import Any
from datetime import datetime, date, time

import json


class Serialize(json.JSONEncoder):
    def default(self, field: Any) -> Any:
        if isinstance(field, (datetime, date, time)):
            if isinstance(field, datetime):
                return field.isoformat() + 'Z'

            else:
                return field.isoformat()
