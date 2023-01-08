class DB:
    user_name = "root"
    password = "jys1013011!"
    host_url = "localhost"
    port_num = "3306"
    db_name = "yeonseo"
    db_url = f'mysql+pymysql://{user_name}:{password}@{host_url}:{port_num}/{db_name}?charset=utf8mb4'
    
class Quarters:
    quarters = {
        # 2022
        "2022__Q2": "Q202211012",
        "2022__Q1": "Q202211013",
        
        # 2021
        "2021__Q4": "Q202111011",
        "2021__Q3": "Q202111014",
        "2021__Q2": "Q202111012",
        "2021__Q1": "Q202111013",
        
        # 2020
        "2020__Q4": "Q202011011",
        "2020__Q3": "Q202011014",
        "2020__Q2": "Q202011012",
        "2020__Q1": "Q202011013",
        
        # 2019
        "2019__Q4": "Q201911011",
        "2019__Q3": "Q201911014",
        "2019__Q2": "Q201911012",
        "2019__Q1": "Q201911013",
        
        # 2018
        "2018__Q4": "Q201811011",
        "2018__Q3": "Q201811014",
        "2018__Q2": "Q201811012",
        "2018__Q1": "Q201811013",
    }
    
JWT_SECRET = "ABCD1234!"
JWT_ALGORITHM = "HS256"
EXCEPT_PATH_LIST = ["/", "/openapi.json"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/auth|/static|/test)"
MAX_API_KEY = 3
MAX_API_WHITELIST = 10