import logging

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',   # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[91m',  # Red
        'RESET': '\033[0m'    # Reset color
    }

    def format(self, record):
        log_message = super().format(record)
        log_message = self.COLORS.get(record.levelname, '') + log_message + self.COLORS['RESET']
        return log_message


def get_logger(log_file="Log.log"):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the logging level to the lowest (DEBUG)

    # Create a console handler for displaying log messages to the user
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Set the console handler's logging level (INFO or higher)

    # Create formatter for the log messages
    colored_formatter = ColoredFormatter(fmt="%(asctime)s [%(levelname)s]: %(message)s",
                                         datefmt="%Y-%m-%d %H:%M:%S")

    # Set the formatter the handler
    console_handler.setFormatter(colored_formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger