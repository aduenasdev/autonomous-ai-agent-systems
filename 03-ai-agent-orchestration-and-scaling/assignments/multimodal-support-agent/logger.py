import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)

def log_event(message: str):
    logging.info(message)
