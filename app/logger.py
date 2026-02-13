import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(clientip)s | %(message)s",
    )
    return logging.getLogger("SimpleWebServer")
