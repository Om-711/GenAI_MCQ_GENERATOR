from datetime import datetime
import os
import logging

timestamp = datetime.now().strftime("%d-%m-%Y__%H-%M-%S") 

log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
