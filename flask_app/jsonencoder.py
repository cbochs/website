import json
from datetime import datetime

from flask_pymongo import ObjectId

from flask_app.formatter.datetime import DATETIME_FORMAT_ECMA


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return datetime.strftime(o, DATETIME_FORMAT_ECMA)
        return json.JSONEncoder.default(self, o)
