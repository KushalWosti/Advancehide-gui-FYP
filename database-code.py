from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

database_url = 'postgres://kushal:localhost:57902/browser/'

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
    email = Column(String())
    first_name = Column(String())
    middle_name = Column(String())
    last_name = Column(String())
    is_active = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)
print("sql alchemy runned successfully")

sandip_json = {"email": "sandipneupane65@gmail.com", "first_name": "sandip", "middle_name": "No middle Name",
               "last_name": "neupane", "is_active": True}
kushal_json = {"email": "kushal65@gmail.com", "first_name": "kushal", "middle_name": "wosti", "last_name": "wosti",
               "is_active": False}


def create_user(user_json):
    db_session = get_session()

    email = user_json.get("email")
    first_name = user_json.get("first_name")
    middle_name = user_json.get("middle_name")
    last_name = user_json.get("last_name")
    is_active = user_json.get("is_active")

    user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        is_active=is_active
    )

    db_session.add(user)
    db_session.commit()


def update_user(user_id, user_json):
    db_session = get_session()

    email = user_json.get("email")
    first_name = user_json.get("first_name")
    middle_name = user_json.get("middle_name")
    last_name = user_json.get("last_name")
    is_active = user_json.get("is_active")

    users_query = db_session.query(User).filter(User.id == user_id).all()
    if users_query:
        user = users_query[0]
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if middle_name:
            user.middle_name = middle_name
        if is_active is not None:
            user.is_active = is_active

        db_session.add(user)
        db_session.commit()
    else:
        return {"message": "User with {} does not exists".format(user_id)}


def delete_user(user_id):
    db_session = get_session()
    user = db_session.query(User).filter(User.id == user_id).delete()
    db_session.commit()

    return {"message": "User is deleted successfully"}


if __name__ == "__main__":
    # create_user(sandip_json)
    # print("User Sandip is created Successfully")
    # update_user(1, kushal_json)
    # print("User Sandip is updated Successfully")
    delete_user(1)
    print("user deleted successfully")

