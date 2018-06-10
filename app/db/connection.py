from app.db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONFIG = {
    'USER': 'root',
    'HOST': 'localhost',
    'DB': 'foo',
}

ENGINE = create_engine('mysql://{USER}@{HOST}/{DB}'.format(**DB_CONFIG))

Base.metadata.create_all(ENGINE)

Session = sessionmaker(bind=ENGINE)

session = Session()
