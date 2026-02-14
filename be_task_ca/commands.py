from .database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from .item.adapters.db.model import Item
from .user.adapters.db.model import CartItem, User


def create_db_schema():
    Base.metadata.create_all(bind=engine)
