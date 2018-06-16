from app.db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# DB_CONFIG = {'USER': 'root', 'HOST': 'localhost', 'DB': 'bar' }
# engine = create_engine('mysql://{USER}@{HOST}/{DB}'.format(**DB_CONFIG))
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
