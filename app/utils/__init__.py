import os

from app.utils.logger import setup_logger

if not os.path.isdir('/app/runtime'):
    os.makedirs('/app/runtime')

logger = setup_logger("sys", "INFO", '/app/runtime/sys.log', day_rotating=True)