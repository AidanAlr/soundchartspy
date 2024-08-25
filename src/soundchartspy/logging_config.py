import logging
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s [Line: %(lineno)d in %(filename)s]')
console_handler.setFormatter(formatter)

# Create a specific logger
main_logger = logging.getLogger('main_logger')
main_logger.addHandler(console_handler)
main_logger.setLevel(logging.INFO)

test_logger = logging.getLogger('test_logger')
test_logger.addHandler(console_handler)
test_logger.setLevel(logging.DEBUG)