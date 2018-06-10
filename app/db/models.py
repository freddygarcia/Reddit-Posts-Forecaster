from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP

Base = declarative_base()


class Post(Base):
    '''Define model to data persistence'''

    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False)
    content = Column(String(220), nullable=False)
    permalink = Column(String(120), nullable=False)

    def to_dict(self):
        return {
            'created_at': self.created_at,
            'content': self.content,
            'permalink': self.permalink
        }
