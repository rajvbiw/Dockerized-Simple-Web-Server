import os

HOST = os.getenv("APP_HOST", "0.0.0.0")
PORT = int(os.getenv("APP_PORT", 9090))
ENV  = os.getenv("ENV", "production")
