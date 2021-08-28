import json

class jsonify:
    def __init__(self, data):
        self.jsonify = data

    def __getattr__(self, attr):
        value = self.jsonify.get(attr)
        if isinstance(value, (list, dict)):
            return jsonify(value)
        return value

    def __getitem__(self, index):
        value = self.jsonify[index]
        if isinstance(value, (list, dict)):
            return jsonify(value)
        return value

    def __setitem__(self, index, value):
        self.jsonify[index] = value

    def __delattr__(self, index):
        self.jsonify.pop(index)

    def __delitem__(self, index):
        self.jsonify.pop(index)

    def __repr__(self):
        return json.dumps(self.jsonify, indent=2, default=lambda x: str(x))


