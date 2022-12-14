import sys
from os import path

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import (
    Integer,
    String,
    Float,
    DateTime,
    Enum,
    Boolean,
)
from sqlalchemy.orm import relationship

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.database.conn import Base
from app.database.orm import BaseMixin

class Stocks(Base, BaseMixin):
    __tablename__ = "stocks"
    __table_args__ = {'extend_existing': True} 
    
    stock_code = Column(String(length=20), nullable=True, default=None)
    stock_name = Column(String(length=255), nullable=True, default=None)
    market = Column(String(length=20), nullable=True, default=None)
    close = Column(Float, nullable=True, default=None)
    open = Column(Float, nullable=True, default=None)
    high = Column(Float, nullable=True, default=None)
    low = Column(Float, nullable=True, default=None)
    volume = Column(Float, nullable=True, default=None)
    amounts = Column(Float, nullable=True, default=None)
    market_cap = Column(Float, nullable=True, default=None)
    shares = Column(Float, nullable=True, default=None)
    
class Accounts(Base, BaseMixin):
    __tablename__ = "accounts"
    __table_args__ = {'extend_existing': True} 
    
    account_nm_eng = Column(String(length=255), nullable=True, default=None)
    account_id = Column(String(length=255), nullable=True, default=None)
    account_nm_kor = Column(String(length=255), nullable=True, default=None)
    
class Amounts(Base, BaseMixin):
    __tablename__ = "amounts"
    __table_args__ = {'extend_existing': True} 
    
    account_nm_eng = Column(String(length=255), nullable=True, default=None)
    account_id = Column(String(length=255), nullable=True, default=None)
    account_nm_kor = Column(String(length=255), nullable=True, default=None)
    stock_code = Column(String(length=20), nullable=True, default=None)
    fs_div = Column(String(length=20), nullable=True, default=None)
    sj_div = Column(String(length=20), nullable=True, default=None)
    
    # 2022
    Q202211012 = Column(Float, nullable=True, default=None)
    Q202211013 = Column(Float, nullable=True, default=None)
    # 2021
    Q202111011 = Column(Float, nullable=True, default=None)
    Q202111014 = Column(Float, nullable=True, default=None)
    Q202111012 = Column(Float, nullable=True, default=None)
    Q202111013 = Column(Float, nullable=True, default=None)
    # 2020
    Q202011011 = Column(Float, nullable=True, default=None)
    Q202011014 = Column(Float, nullable=True, default=None)
    Q202011012 = Column(Float, nullable=True, default=None)
    Q202011013 = Column(Float, nullable=True, default=None)
    # 2019
    Q201911011 = Column(Float, nullable=True, default=None)
    Q201911014 = Column(Float, nullable=True, default=None)
    Q201911012 = Column(Float, nullable=True, default=None)
    Q201911013 = Column(Float, nullable=True, default=None)
    # 2018
    Q201811011 = Column(Float, nullable=True, default=None)
    Q201811014 = Column(Float, nullable=True, default=None)
    Q201811012 = Column(Float, nullable=True, default=None)
    Q201811013 = Column(Float, nullable=True, default=None)
    
class Ratios(Base, BaseMixin):
    __tablename__ = "ratios"
    __table_args__ = {'extend_existing': True} 
    
    stock_code = Column(String(length=20), nullable=True, default=None)
    ratio = Column(String(length=255), nullable=True, default=None)
    
    # 2022
    Q202211012 = Column(Float, nullable=True, default=None)
    Q202211013 = Column(Float, nullable=True, default=None)
    # 2021
    Q202111011 = Column(Float, nullable=True, default=None)
    Q202111014 = Column(Float, nullable=True, default=None)
    Q202111012 = Column(Float, nullable=True, default=None)
    Q202111013 = Column(Float, nullable=True, default=None)
    # 2020
    Q202011011 = Column(Float, nullable=True, default=None)
    Q202011014 = Column(Float, nullable=True, default=None)
    Q202011012 = Column(Float, nullable=True, default=None)
    Q202011013 = Column(Float, nullable=True, default=None)
    # 2019
    Q201911011 = Column(Float, nullable=True, default=None)
    Q201911014 = Column(Float, nullable=True, default=None)
    Q201911012 = Column(Float, nullable=True, default=None)
    Q201911013 = Column(Float, nullable=True, default=None)
    # 2018
    Q201811011 = Column(Float, nullable=True, default=None)
    Q201811014 = Column(Float, nullable=True, default=None)
    Q201811012 = Column(Float, nullable=True, default=None)
    Q201811013 = Column(Float, nullable=True, default=None)
    
class Users(Base, BaseMixin):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 
    
    status = Column(Enum("active", "deleted", "blocked"), default="active")
    email = Column(String(length=255), nullable=True)
    pw = Column(String(length=2000), nullable=True)
    name = Column(String(length=255), nullable=True)
    phone_number = Column(String(length=20), nullable=True, unique=True)
    profile_img = Column(String(length=1000), nullable=True)
    sns_type = Column(Enum("FB", "G", "K"), nullable=True)
    marketing_agree = Column(Boolean, nullable=True, default=True)
    
    
class StocksUsers(Base, BaseMixin):
    __tablename__ = "stocks_users"
    __table_args__ = {'extend_existing': True}

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    stock_id = Column(Integer, ForeignKey("stocks.id", ondelete="CASCADE"))
    
class Rates(Base, BaseMixin):
    __tablename__ = "rates"
    __table_args__ = {'extend_existing': True}
    
    stock_code = Column(String(length=20), nullable=True, default=None)
    account_nm_eng = Column(String(length=255), nullable=True, default=None)
    account_nm_kor = Column(String(length=255), nullable=True, default=None)
    QoQ = Column(Float, nullable=True, default=None)
    YoY = Column(Float, nullable=True, default=None)
    
class Factors(Base, BaseMixin):
    __tablename__ = "factors"
    __table_args__ = {'extend_existing': True}
    
    stock_code = Column(String(length=20), nullable=True, default=None)
    stock_name = Column(String(length=255), nullable=True, default=None)
    account_nm_eng = Column(String(length=255), nullable=True, default=None)
    amounts = Column(Float, nullable=True, default=None)
    market_cap = Column(Float, nullable=True, default=None)
    factor = Column(String(length=20), nullable=True, default=None)
    factor_value = Column(Float, nullable=True, default=None)

# stocks_users = Table(
#     "stocks_users",
#     Base.metadata,
#     Column("left_id", ForeignKey("left_table.id"), primary_key=True),
#     Column("right_id", ForeignKey("right_table.id"), primary_key=True),
# )


# class Parent(Base):
#     __tablename__ = "left_table"
#     id = Column(Integer, primary_key=True)
#     children = relationship(
#         "Child", secondary=association_table, back_populates="parents"
#     )


# class Child(Base):
#     __tablename__ = "right_table"
#     id = Column(Integer, primary_key=True)
#     parents = relationship(
#         "Parent", secondary=association_table, back_populates="children"
#     )