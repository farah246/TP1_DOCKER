import os
import socket
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host=os.environ.get("REDIS_HOST", "db-service"), port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError:
            if retries == 0:
                raise
            retries -= 1
            time.sleep(0.5)


@app.route("/")
def hello():
    count = get_hit_count()
    return f"Bonjour ! Cette page a été vue {count} fois. Je suis le conteneur {socket.gethostname()}\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)