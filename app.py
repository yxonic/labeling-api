__version__ = "0.0.1"

import pymongo
from util import *
from flask import Flask, request

app = Flask(__name__)
mongo = pymongo.MongoClient("mongodb://172.16.46.202:27017/",
                            serverSelectionTimeoutMS=1000)
db = mongo.labeling


@app.route('/')
@api
def version():
    return {"version": __version__}


@app.route('/<dataset>', methods=['GET'])
@api
def get_schema(dataset):
    schema = db.schemas.find_one({"dataset": dataset})
    if not schema:
        raise KeyError('schema not found')
    del schema['_id']
    return schema


@app.route('/<dataset>', methods=['POST'])
@api
def update_schema(dataset):
    schema = request.json
    r = db.schemas.replace_one({"dataset": dataset},
                               dict(dataset=dataset, **schema),
                               upsert=True)
    return {"acknowledged": r.acknowledged}


@app.route('/<dataset>/page/<int:page>', methods=['GET'])
@api
def get_page(dataset, page):
    return {"func": "get_page", "dataset": dataset, "page": page}


@app.route('/<dataset>/<itemid>', methods=['GET'])
@api
def get_item(dataset, itemid):
    return {"func": "get_item", "dataset": dataset, "item": itemid}


@app.route('/<dataset>/<itemid>', methods=['POST'])
@api
def update_item(dataset, itemid):
    return {"func": "update_item", "dataset": dataset, "item": itemid,
            "content": request.json}
