from dataclasses import dataclass, asdict
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    
    
    user_name = "root"
    password = "jys9807!"
    host_url = "localhost"
    port_num = "3306"
    db_name = "yeonseo"
    db_url = f'mysql+pymysql://{user_name}:{password}@{host_url}:{port_num}/{db_name}?charset=utf8mb4'
    DB_URL: str = environ.get("DB_URL", db_url)



@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))

if __name__ == "__main__":
    print("\n\n", asdict(conf()), "\n\n")