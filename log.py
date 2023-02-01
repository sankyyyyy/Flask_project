import logging
def start():
    logging.basicConfig(filename="logfile.log",
                        format="%(asctime)s %(message)s",
                        filemode="w")

    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)

    logger.debug("debug message")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
