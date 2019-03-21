from flask.json import JSONEncoder


class PhraseBookJSONEncoder(JSONEncoder):

    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        else:
            return JSONEncoder.default(self, obj)
