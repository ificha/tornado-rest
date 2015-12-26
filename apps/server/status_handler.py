
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
import json

class StatusHandler(APIHandler):

    @schema.validate(
        output_schema={
            "type": "object",
             "properties": {
                "status": {"type": "string"},
            }
        },
    )
    def get(self):

        return {"status": "ok"}
