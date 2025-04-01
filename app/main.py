from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Header
from sqlmodel import Session, select

from app.models.models import User
from app.schemas.user_schemas import CreateUser, ExcludeInfo
from app.database.database import create_db_and_tables, engine
from app.database.password_hashing import create_hash_password


API_KEY = "api123api"


# Using this dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.get("/")
def root():
    return {"Pranjal's Project": "FastAPI CRUD App"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Add one record using POST
@app.post("/users/")
def add_new_user(
        user: CreateUser,
        session: SessionDep,
        x_api_key: str = Header(None, convert_underscores=False)
) -> User:

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key used, please use valid api key")

    hashed_password = create_hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# Read all data of users
@app.get("/users/", response_model=list[ExcludeInfo])
def get_all_users_data(session: SessionDep) -> list[User]:
    all_users = session.exec(select(User)).all()
    if not all_users:
        raise HTTPException(status_code=404, detail="No data present in the table for the users")
    return all_users


# Read one record from the table
@app.get("/users/{user_id}", response_model=ExcludeInfo)
def get_user_data(user_id: int, session: SessionDep) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="This user is not present in the database")
    return user


# Delete one user from the User model table
@app.delete("/users/{user_id}")
def delete_user(
        user_id: int,
        session: SessionDep,
        x_api_key: str = Header(None, convert_underscores=False)):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key used, please use valid api key")

    user_to_delete = session.get(User, user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User you are trying to delete is not present in the database")

    session.delete(user_to_delete)
    session.commit()
    return {f"user with id {user_id} deleted from database": True}


# Update user information in the database
@app.put("/users/{user_id}")
def update_user(
        user_data: CreateUser,
        user_id: int,
        session: SessionDep,
        x_api_key: str = Header(None, convert_underscores=False)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key used, please use valid api key")

    hashed_password = create_hash_password(user_data.password)

    user_to_update = session.get(User, user_id)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User you are trying to update is not present in the database")

    user_to_update.name = user_data.name
    user_to_update.email = user_data.email
    user_to_update.password = hashed_password

    session.commit()
    session.refresh(user_to_update)
    return {f"Successfully updated information for user with id {user_id}": True}
