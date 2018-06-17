from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class Post(Base):
    '''Define model to data persistence'''

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False)
    permalink = Column(String(120), nullable=False, unique=True)

    def to_dict(self):
        return {
            'created_at': self.created_at,
            'permalink': self.permalink
        }
