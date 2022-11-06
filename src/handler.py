import os
import json
import redis
import random
from src.util import construct_signup_email_verification_redis_key
from src.send_email import send_signup_verification_email

from dotenv import load_dotenv
load_dotenv()


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASS = os.environ.get("REDIS_PASS")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS)


def signup_handler(msg):
    value = json.loads(msg.value())
    email = value['email']
    username = value['username']
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    send_signup_verification_email("CrossCopy Sign Up Email Verification", code, email)
    key = construct_signup_email_verification_redis_key(username, email, code)
    redis_client.hset(key, "status", "not-verified")
    redis_client.hset(key, "chance-left", str(2))  # Number of chance to fail, TODO: use a env var
    redis_client.expire(key, 10 * 60)        # expire in 10 minutes TODO: use an env var