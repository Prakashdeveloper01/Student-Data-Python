from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

Base = declarative_base()

DATABASE_URL = 'mysql+pymysql://root:root@localhost/student'

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit = False , autoflush= False , bind = engine)

Base.metadata.create_all(bind=engine)