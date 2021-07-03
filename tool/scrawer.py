"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     scrawer.py
@Author:   shenfan
@Time:     2020/10/20 17:40
"""
import logging
from logging.handlers import RotatingFileHandler
# import sys
# logging.basicConfig(level=logging.DEBUG,format="%(asctime)s *** %(filename)s *** %(levelname)s *** %(message)s *** %(levelno)s *** %(pathname)s *** %(funcName)s *** %(lineno)s *** %(thread)d *** %(threadName)s *** %(process)d",datefmt="%Y-%m-%d %X",filename="log1.txt")
# logger = logging.getLogger(__name__)
# logger.info("Start print log")
# logger.debug("Do something")
# logger.warning("Something maybe fail.")
# logger.info("Finish")

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = RotatingFileHandler("log.txt",maxBytes=1*1024,backupCount=3)
handler.setLevel(level=logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(lineno)s --- %(message)s"))

console = logging.StreamHandler()
console.setLevel(logging.WARNING)

logger.addHandler(handler)
logger.addHandler(console)

logger.info("xxxxxxxxxxxxxxx")
logger.debug("Do something")
logger.warning("Something maybe fail.")
logger.info("Finish")
try:
    open("xxx.log","rb")
except (SystemExit,KeyboardInterrupt):
    raise
except Exception:
    logger.exception("Failed to open sklearn.txt from logger.exception")





