from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Translation(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_language = Column(String(50), nullable=False)
    target_language = Column(String(50), nullable=False)
    input_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Замените <username>, <password>, <hostname> и <database> на реальные значения
DATABASE_URL = 'postgresql://username:password@hostname/database'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def save_translation_to_db(source_language, target_language, input_text, translated_text):
    session = Session()
    new_translation = Translation(
        source_language=source_language,
        target_language=target_language,
        input_text=input_text,
        translated_text=translated_text
    )
    session.add(new_translation)
    session.commit()
    session.close()
