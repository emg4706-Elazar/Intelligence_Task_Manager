import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

filehandler = logging.FileHandler(r"logs/app.log", encoding="utf-8")
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
