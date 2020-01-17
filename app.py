import os
from time import process_time

from flask import Flask, abort, jsonify
import redis

POD_NAME = os.getenv('POD_NAME')
NODE_NAME = os.getenv('NODE_NAME')
POD_IP = os.getenv('POD_IP')
REDIS_HOST = os.getenv('REDIS_HOST')

r = redis.Redis(host=REDIS_HOST)

app = Flask(__name__)

@app.route("/")
def index():
    return "Hey! I'm %s, running on node %s with ip %s" % (POD_NAME, NODE_NAME, POD_IP)

@app.route("/faketimeout")
def fake_gateway_timeout_error():
    abort(504)

@app.route("/create/<key>/<value>")
def create(key, value):
    start_time = process_time()
    r.mset({key: value})
    stop_time = process_time()
    time_elapsed = stop_time - start_time
    return jsonify(time_elapsed=time_elapsed, status="created", key_created=key, value_created=value, node=NODE_NAME, pod=POD_NAME)

@app.route("/get/<key>")
def get(key):
    start_time = process_time()
    result = r.get(key)
    stop_time = process_time()
    time_elapsed = stop_time - start_time

    if not result:
        abort(404)
    return jsonify(time_elapsed=time_elapsed, status="get", key_created=key, response=result, node=NODE_NAME, pod=POD_NAME)

@app.route("/delete/<key>")
def delete(key):
    start_time = process_time()
    r.delete(key)
    stop_time = process_time()
    time_elapsed = stop_time - start_time
    return jsonify(time_elapsed=time_elapsed, status="deleted", key_deleted=key, node=NODE_NAME, pod=POD_NAME)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
