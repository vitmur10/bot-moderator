import pyowm
from pyowm.utils.config import get_default_config

Token_bot = '5487187254:AAGMpUk6wz5zMrrcd9hAV7PwTgThslLCUlg'
config_dict = get_default_config()
config_dict['language'] = 'ua'
owm = pyowm.OWM('22e6da91f40d1f3009f309ebc89a1c5f', config_dict)