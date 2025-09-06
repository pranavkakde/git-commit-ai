import logging

# Create a custom logger
file_logger = logging.getLogger(__name__)
file_logger.setLevel(logging.DEBUG)  # Set the logger's overall level

# Create a file handler
file_handler = logging.FileHandler('gitlog.log', mode='a')  # 'a' for append mode
file_handler.setLevel(logging.DEBUG)  # Set the handler's level

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
file_logger.addHandler(file_handler)