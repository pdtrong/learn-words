import logging
from datetime import datetime as mdt

time_now_str = mdt.now().strftime('%y%m%d_%H%M%S')
file_name = 'migrate_{}.log'.format(time_now_str)

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

c_format = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%y%m%d_%H%M%S')
c_handler = logging.StreamHandler()
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

# f_format = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%y%m%d_%H%M%S')
# f_handler = logging.FileHandler(file_name)
# f_handler.setLevel(logging.INFO)
# f_handler.setFormatter(f_format)
# logger.addHandler(f_handler)
