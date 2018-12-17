__version__ = "0.0.1"

import pymongo
import math
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


@app.route('/<dataset>', methods=['PUT'])
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
    cursor = db[dataset].find().skip(50 * (page - 1)).limit(50)  # page conf
    documents = [{k: v for k, v in doc.items() if k != '_id'}
                 for doc in cursor]
    return {"documents": documents,
            "total": math.ceil(db[dataset].count() / 10)}


@app.route('/<dataset>/<itemid>', methods=['GET'])
@api
def get_item(dataset, itemid):
    item = db[dataset].find_one({'id': itemid})
    if not item:
        raise KeyError('item not found')
    del item['_id']
    return item


@app.route('/<dataset>/<itemid>', methods=['PUT'])
@api
def update_item(dataset, itemid):
    document = request.json
    r = db[dataset].replace_one({'id': itemid}, dict(id=itemid, **document),
                                upsert=True)
    return {"acknowledged": r.acknowledged}
