import logging
import colorlog

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[41m", # Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"
    
def set_logger(level: int = logging.INFO) -> None:
    handler = colorlog.StreamHandler()

    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s:%(name_log_color)s%(name)s%(reset)s:%(message)s",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red,bg_white',
        },
        secondary_log_colors={
            'name': {
                'DEBUG':    'blue',
                'INFO':     'black',
                'WARNING':  'blue',
                'ERROR':    'blue',
                'CRITICAL': 'blue',
            }
        }
    )

    handler.setFormatter(formatter)

    root = logging.getLogger()
    if not root.handlers:  # avoid adding multiple handlers if already configured
        root.addHandler(handler)
    root.setLevel(level)
