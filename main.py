import os
import sys
from threads import ClientProcess
import configloader
import logging
from logging import handlers
from threading import Event

def main():
    c = configloader.config()
    event = Event()
    logging.basicConfig(
        level=getattr(logging,c.getkey("log_level")), format="%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s"
    )
    if c.getkey("log_file") != "" and c.getkey("log_file") is not None:
        file_log_handler = handlers.RotatingFileHandler(c.getkey("log_file"), mode="a", encoding=c.getkey("log_file_encoding"), maxBytes=c.getkey("log_file_size"), backupCount=c.getkey("log_file_backup_count"))
        formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s")
        file_log_handler.setFormatter(formatter)
        file_log_handler.setLevel(getattr(logging,c.getkey("log_level")))
        logging.getLogger('').addHandler(file_log_handler)
    if c.getkey("log_error_file") != "" and c.getkey("log_error_file") is not None:
        file_error_handler = handlers.RotatingFileHandler(c.getkey("log_error_file"), mode="a", encoding=c.getkey("log_file_encoding"), maxBytes=c.getkey("log_file_size"), backupCount=c.getkey("log_file_backup_count"))
        formatter = logging.Formatter("%(asctime)s [%(levelname)s][%(pathname)s:%(lineno)d]: %(message)s")
        file_error_handler.setFormatter(formatter)
        file_error_handler.setLevel(getattr(logging,c.getkey("log_error_level")))
        logging.getLogger('').addHandler(file_error_handler)
    logging.info("Starting process")
    p = ClientProcess.ClientProcess()
    p.start()
    while(p.is_alive()):
        try:
            p.join(10)
        except (KeyboardInterrupt, SystemExit, SystemError):
            p.stop()
            logging.info("Stopping process")
            break
        except:
            import traceback
            logging.error("Error in main thread")
            logging.error(traceback.format_exc())
            break

if __name__ == "__main__":
    main()