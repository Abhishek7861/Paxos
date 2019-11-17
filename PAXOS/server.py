import logging
import output

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger(__name__)

output.print_success(logger.debug("This is a debug log"))
logger.info("This is an info log")
logger.critical("This is critical")
logger.error("An error occurred")