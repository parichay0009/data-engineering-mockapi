from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Text,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base

from config import Config


class DBINIT:
    """
    This class is to initiate the database engine so that it can be used in any part pf application.
    """

    def __init__(self) -> None:
        self.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)


Base = declarative_base()


class User(Base):
    """
    This class is for storing all the user details in database.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    birth_date = Column(DateTime)
    email = Column(Text)
    city = Column(Text)
    gender = Column(Text)
    income = Column(Float)
    profession = Column(Text)
    zip_code = Column(Text)
    is_smoking = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Subscriptions(Base):
    __tablename__ = "subscriptions"
    """
    This class holds the information about the users subscription.
    """

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, primary_key=True)
    amount = Column(Float)
    status = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)


class Messages(Base):
    """
    This class stores the massages from sender to receiver
    """

    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    created_at = Column(DateTime)


try:
    Base.metadata.create_all(DBINIT().engine)
except:
    pass
