from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#def Load_Data(file_name):
  #  data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s),1: lambda s: str(s),2: lambda s: str(s),3: lambda s: str(s)})
   # return data.tolist()

Base = declarative_base()

class Pharmacies(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'Pharmacies'
    __table_args__ = {'sqlite_autoincrement': True, 'extend_existing':True}
    #tell SQLAlchemy the name of column and its attributes:
	id = Column(Integer, primary_key=True, nullable=False) 
    name = Column(String) 
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)


engine = create_engine("sqlite:///pharma_test.db")
Base.metadata.create_all(engine)

file_name = 'pharmacies.csv'
df = pandas.read_csv(file_name)
df.to_sql(con=engine, index_label='address', name=Pharmacies.__tablename__, if_exists='append')