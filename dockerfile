FROM python:3.12-slim

WORKDIR /app

COPY app/ app/
COPY html/ html/
COPY requirements.txt .

EXPOSE 9090
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9090/health')"
CMD ["python", "app/server.py"]
