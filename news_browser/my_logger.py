# Standard Python library imports
import logging

# Here we create a logger
logger = logging.getLogger('challenge_logger')
logger.setLevel(logging.DEBUG)  # Nivel global del logger

# We create a handler for the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Nivel específico para la consola

# We create a format and assign it to the console handler
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
console_handler.setFormatter(console_format)

# We add the handler to the console
logger.addHandler(console_handler)

# Here we create a handler for the files
file_handler = logging.FileHandler('output/formatted_log_for_challenge.log')
file_handler.setLevel(logging.DEBUG)  # We specify the level for the file (If we want everything, so DEBUG)

# We create a format and assign it to the files handler
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')
file_handler.setFormatter(file_format)

# Finally we add the file handler to the logger
logger.addHandler(file_handler)
