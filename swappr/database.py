import sqlalchemy as sa
import sqlalchemy.orm as sao
from . import app
import swappr
import os.path

engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                          convert_unicode=True)

db_session = sao.scoped_session(sao.sessionmaker(bind=engine))
Base = swappr.Base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)

if (not os.path.isfile('swappr.db')):
	print("Creating the database in this local directory called swappr.db")
	init_db()