
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema

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
        self.success({"status": "ok"})
