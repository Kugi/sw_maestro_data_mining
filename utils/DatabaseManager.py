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


    class Cache_query(__BaseObj__):
        __tablename__ = 'query_freq'
        query = Column('query', String(100), primary_key=True)
        num = Column('num', Integer)
        update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
        def __init__(self,query,num):
            self.query=query
            self.num=num

    class Cache_pmi(__BaseObj__):
        __tablename__ = 'app_keyword_pmi'
        app_id = Column('app_id', Integer, primary_key=True)
        keyword = Column('keyword', String(100), primary_key=True)
        pmi = Column('pmi', Float)
        update_date = Column('update_date', Date(),default=datetime.now(), onupdate=datetime.now())
        def __init__(self,app_id,keyword,pmi):
            self.app_id=app_id
            self.keyword=keyword
            self.pmi=pmi


    @staticmethod
    def create_table():
        '''
        recreate a new table.
        '''
        if DatabaseManager.__db__.dialect.has_table(DatabaseManager.__db__.connect(), "query_freq"):
            DatabaseManager.__db__.execute("drop table query_freq;")
        metadata = DatabaseManager.Cache_query.metadata
        metadata.create_all(DatabaseManager.__db__)


    @staticmethod
    def get_query_count(query):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_query).filter(DatabaseManager.Cache_query.query==query)
        #s.flush()
        s.close_all()
        if result.count()>0:
            return result[0].num
        return 0


    @staticmethod
    def set_query_count(query,count):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_query).filter(DatabaseManager.Cache_query.query==query)

        if result.count()>0:
            result[0].num = count
        else:
            s.add(DatabaseManager.Cache_query(query,count))
        s.commit()
        s.close_all()

    @staticmethod
    def get_app_keyword_pmi(app_id, keyword):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_pmi).\
            filter(DatabaseManager.Cache_pmi.app_id==app_id).\
            filter(DatabaseManager.Cache_pmi.keyword==keyword)
        if result.count()>0:
            return result[0].num
        return 0

    @staticmethod
    def set_app_keyword_pmi(app_id, keyword, pmi):
        s = DatabaseManager.__Session__()
        result = s.query(DatabaseManager.Cache_pmi).\
            filter(DatabaseManager.Cache_pmi.app_id==app_id).\
            filter(DatabaseManager.Cache_pmi.keyword==keyword)
        if result.count()>0:
            result[0].pmi = pmi
        else:
            s.add(DatabaseManager.Cache_pmi(app_id, keyword, pmi))
        s.commit()
