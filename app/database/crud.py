import sys
from os import path
import pandas as pd

from dataclasses import asdict
from sqlalchemy import Column, func
from sqlalchemy import select
from sqlalchemy.types import Integer, DateTime
from sqlalchemy.orm import Session

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.common.config import conf
from app.database.conn import db

c = conf()
conf_dict = asdict(c)
db.init_db(**conf_dict)

def get_filter(model, columns: list = None, **kwargs):
    """Get data (select `columns` from `table` where `cond`)

    Args:
        model: database.models.model
        kwargs (dict): {"column__operator": "value"}
        ** operator
            - 'gt': >
            - 'gte': >=
            - 'lt': <
            - 'lte': <=
            - 'in': in_

    Returns:
        result (list[object]): query result
    """
    sess = next(db.session())
    
    if columns is None:
        cols = [model]
    else:
        cols = list(map(lambda x: getattr(model, x), columns))

    cond = []
    for key, val in kwargs.items():
        key = key.split("__")
        col = getattr(model, key[0])
        if len(key) == 1: cond.append((col == val))
        elif len(key) == 2 and key[1] == 'gt': cond.append((col > val))
        elif len(key) == 2 and key[1] == 'gte': cond.append((col >= val))
        elif len(key) == 2 and key[1] == 'lt': cond.append((col < val))
        elif len(key) == 2 and key[1] == 'lte': cond.append((col <= val))
        elif len(key) == 2 and key[1] == 'in': cond.append((col.in_(val)))
    
    result = sess.execute(
        select(*cols)
    ).fetchall()
    
    return result

def convert_df(model, **kwargs):
    
    result = get_filter(model, **kwargs)
    result_dict = list(map(lambda x: x[0].__dict__, result))
    result_df = pd.DataFrame(result_dict)
    
    return result_df

# def get_all(model):
#     """Get table all data

#     Args:
#         model: Model
#         db: BaseMixin (Session)
#     """
#     sess = next(db.session())
#     obj = sess.query(model).all()
    
#     if sess is not None:
#         sess.close()
    
#     return obj

# def get_filter(model, stock_code: str or list):
#     sess = next(db.session())
#     query = sess.query(model)
#     if type(stock_code) == str:
#         obj = query.filter(model.stock_code==stock_code).all()
#     elif type(stock_code) == list:
#         if len(stock_code) == 1:
#             stock_code = stock_code[0]
#             obj = query.filter(model.stock_code==stock_code).all()
#         else:
#             obj = query.filter(model.stock_code.in_(stock_code)).all()
#     else:
#         raise TypeError("stock_code type error")
        
#     return obj

# def get(model, **kwargs):
#     sess = next(db.session())
#     objs = sess.get(model, kwargs)
        
#     return objs