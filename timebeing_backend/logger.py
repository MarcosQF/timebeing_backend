import logging
import sys

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Ensure auth middleware logs are visible
auth_logger = logging.getLogger('timebeing_backend.auth_middleware')
auth_logger.setLevel(logging.INFO)
