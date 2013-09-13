__author__ = 'kugi'

from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DatabaseManager():

    __BaseObj__ = declarative_base()
    __db__ = create_engine('postgresql://soma:maestro@)!#@soma1.buzzni.com/application')
    __Session__ = sessionmaker(bind=__db__)
    #__s__ = __Session__()

    #__db__.echo = False  # Try changing this to True and see what happens
    #__metadata__ = MetaData(__db__)

    class Cache(__BaseObj__):
        __tablename__ = 'query_freq'
        query = Column('query', String(100), primary_key=True)
        num = Column('num', Integer)
        update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
        def __init__(self,query,num):
            self.query=query
            self.num=num


    @staticmethod
    def _get_date():
        return datetime.datetime.now()


    @staticmethod
    def create_table():
        '''
        recreate a new table.
        '''
        if DatabaseManager.__db__.dialect.has_table(DatabaseManager.__db__.connect(), "query_freq"):
            DatabaseManager.__db__.execute("drop table query_freq;")
        metadata = DatabaseManager.Cache.metadata
        metadata.create_all(DatabaseManager.__db__)


    @staticmethod
    def query_count(query):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache).filter(DatabaseManager.Cache.query==query)
        #s.flush()
        s.close_all()
        if result.count()>0:
            return result[0].num
        return 0


    @staticmethod
    def set_query_count(query,count):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache).filter(DatabaseManager.Cache.query==query)

        if result.count()>0:
            result[0].num = count
        else:
            s.add(DatabaseManager.Cache(query,count))
        s.commit()
        s.close_all()


