from sqlalchemy.orm import Session
 
# from app.schemas.users import UserCreate
# from app.curd.curd_users import crud_users
# from app.core.config import settings
 
 
# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
 
 
# def init_db(db: Session) -> None:
#     # Tables should be created with Alembic migrations
#     # But if you don't want to use migrations, create
#     # the tables un-commenting the next line
#     # Base.metadata.create_all(bind=engine)
 
#     user = crud_users.get_user_by_email(db, email=settings.FIRST_SUPERUSER)
#     if not user:
#         user_in = UserCreate(
#             email=settings.FIRST_SUPERUSER,
#             password=settings.FIRST_SUPERUSER_PASSWORD,
#             is_superuser=True,
#         )
#         user = crud_users.user_create(db, obj_in=user_in)