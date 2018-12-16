from functools import wraps
from flask import jsonify


def api(f):
    @wraps(f)
    def new_f(*args, **kwargs):
        try:
            res = jsonify(f(*args, **kwargs))
        except Exception as e:
            res = jsonify({"error": str(e).strip('\'')})
        return res
    return new_f
