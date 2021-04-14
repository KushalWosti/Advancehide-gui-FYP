from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from sqlalchemy import true
database_url = 'postgresql://postgres:kushal@localhost/datahiding'

Base = declarative_base()

engine = create_engine(database_url, convert_unicode=True)


def get_session():
    return scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))


Base.query = get_session().query_property()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(), unique=True)
    full_name = Column(String())
    email = Column(VARCHAR(), nullable=False)
    username = Column(String(), unique=True)
    password = Column(VARCHAR(), nullable=False)
    gender = Column(String, nullable=False)
    joining_date = Column(DateTime(), default=datetime.now())
    phone_number = Column(String(), nullable=False)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)


class File(Base):
    __tablename__ = 'files'
    file_id = Column(Integer, primary_key=True)
    sender_ = Column(VARCHAR, ForeignKey('users.username'))
    file_name = Column(VARCHAR)
    file_type = Column(String)
    send_date = Column(DateTime(), default=datetime.now())


Base.metadata.create_all(bind=engine)
print("sql alchemy runned successfully")


def sign_up(user_detail):
    db_session = get_session()
    uuid = user_detail.get("uuid")
    full_name = user_detail.get("full_name")
    email = user_detail.get("email")
    gender = user_detail.get("gender")
    username = user_detail.get("username")
    password = user_detail.get("password")
    phone_number = user_detail.get("phone_num")

    user = db_session.query(User).all()

    if user:
        user = User(
            uuid=uuid,
            full_name=full_name,
            email=email,
            gender=gender,
            username=username,
            password=password,
            phone_number=phone_number,
        )

    else:
        user = User(
            uuid=uuid,
            full_name=full_name,
            gender=gender,
            email=email,
            username=username,
            password=password,
            phone_number=phone_number,
            is_admin=True,
            is_active=True
        )

    db_session.add(user)
    db_session.commit()


def qry_sign_in(username, password):
    db_session = get_session()
    user = db_session.query(User).filter(User.username == username, User.password == password,
                                         User.is_active == true()).first()
    uuid = user.uuid
    if user:
        is_admin = user.is_admin # either true or false
        if is_admin:
            return {"sign_in": True, "is_admin": True, "uid": uuid}
        else:
            return {"sign_in": True, "is_admin": False, "uid": uuid}
    else:
        return {"sign_in": False, "is_admin": False}


def qry_remove_user(username):
    db_session = get_session()
    user = db_session.query(User).filter(User.username == username).first()
    db_session.delete(user)
    db_session.commit()


def qry_add_admin(username):
    db_session = get_session()
    user = db_session.query(User).filter(User.username == username).first()
    user.is_admin = True
    db_session.commit()


def qry_activate_user(username):
    db_session = get_session()
    user = db_session.query(User).filter(User.username == username).first()
    user.is_active = True
    db_session.commit()


def qry_remove_admin(username):
    db_session = get_session()
    user = User.query(User).filter(User.username == username).first()
    user.is_active = False
    db_session.commit()



if __name__ == "__main__":
  pass
