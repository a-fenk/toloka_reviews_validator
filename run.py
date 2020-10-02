from config import Config
from validate_config import check_config
from validator import run_validation


if __name__ == '__main__':
    if check_config(Config):
        run_validation()
