from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, signal, sys
from logger import setup_logger
from config import HOST, PORT, ENV

logger = setup_logger()
HTML_DIR = "html"

class SimpleWebServer(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        logger.info(
            format % args,
            extra={"clientip": self.client_address[0]}
        )

    def do_GET(self):
        try:
            routes = {
                "/": self.home,
                "/json": self.json_response,
                "/health": self.health_check,
                "/about": lambda: self.html_file("about.html"),
            }
            routes.get(self.path, self.not_found)()

        except Exception as e:
            logger.error(f"Unhandled error: {e}")
            self.internal_error()

    # ---------- ROUTES ----------

    def home(self):
        self.respond(200, "text/html", "<h1>Production Ready Server</h1>")

    def json_response(self):
        data = {
            "service": "simple-web-server",
            "status": "running",
            "environment": ENV
        }
        self.respond(200, "application/json", json.dumps(data))

    def health_check(self):
        data = {"status": "UP"}
        self.respond(200, "application/json", json.dumps(data))

    def html_file(self, filename):
        try:
            with open(os.path.join(HTML_DIR, filename)) as f:
                self.respond(200, "text/html", f.read())
        except FileNotFoundError:
            self.not_found()

    # ---------- RESPONSES ----------

    def respond(self, status, content_type, content):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.end_headers()
        self.wfile.write(content.encode())

    def not_found(self):
        self.respond(404, "text/html", "<h1>404 Not Found</h1>")

    def internal_error(self):
        self.respond(500, "text/html", "<h1>500 Server Error</h1>")


def graceful_shutdown(signal, frame):
    logger.info("Graceful shutdown initiated")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    logger.info(f"Starting server on {HOST}:{PORT}")
    HTTPServer((HOST, PORT), SimpleWebServer).serve_forever()
