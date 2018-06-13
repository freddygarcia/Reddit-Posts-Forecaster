from app.db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONFIG = {
    'USER': 'root',
    'HOST': 'localhost',
    'DB': 'bar',
}



# ENGINE = create_engine('sqlite:///test.db')
# Session = sessionmaker(bind=ENGINE)
# session = Session()

ENGINE_mysl = create_engine('mysql://{USER}@{HOST}/{DB}'.format(**DB_CONFIG))
Base.metadata.create_all(ENGINE_mysl)
Session_mysql = sessionmaker(bind=ENGINE_mysl)
session = Session_mysql()
