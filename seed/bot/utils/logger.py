import sys
from loguru import logger


logger.remove()
logger.add(sink=sys.stdout, format="<blue>[</blue><white>+</white><yellow>]</yellow>"
                                   " ➤  <white><b>{message}</b></white>")
logger = logger.opt(colors=True)
