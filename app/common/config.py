import sys
from os import path, environ
from dataclasses import dataclass, asdict

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.common.consts import DB

@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DB_URL: str = environ.get("DB_URL", DB.db_url)


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    # DB_URL: str = "mysql+pymysql://travis@localhost/notification_test?charset=utf8mb4"
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()



# @dataclass
# class LocalConfig(Config):
#     PROJ_RELOAD: bool = True


# @dataclass
# class ProdConfig(Config):
#     PROJ_RELOAD: bool = False


# def conf():
#     """
#     환경 불러오기
#     :return:
#     """
#     config = dict(prod=ProdConfig(), local=LocalConfig())
#     return config.get(environ.get("API_ENV", "local"))

if __name__ == "__main__":
    print("\n\n", asdict(conf()), "\n\n")