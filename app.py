# KR2: Solotkin
import os
import socket
import redis
from flask import Flask, request

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
STUDENT = os.getenv("STUDENT", "unknown")

def get_redis():
    return redis.Redis(
        host=REDIS_HOST,
        port=6379,
        password=REDIS_PASSWORD,
        decode_responses=True,
        socket_timeout=3
    )

@app.route("/health")
def health():
    return "ok\n"

@app.route("/")
def index():
    r = get_redis()
    hits = r.incr("hits")
    container_id = socket.gethostname()[:12]
    return f"KR2 | {STUDENT} | container {container_id} | hits: {hits}\n"

@app.route("/whoami")
def whoami():
    scheme = request.headers.get("X-Forwarded-Proto", "none")
    client = request.headers.get("X-Real-IP", "none")
    host = request.headers.get("Host", "none")
    return f"scheme: {scheme}\nclient: {client}\nhost: {host}\n"
