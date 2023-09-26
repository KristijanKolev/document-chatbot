# Import all the models, so that Base has them before being imported by Alembic
from database import Base
from models import *
