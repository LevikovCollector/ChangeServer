from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///w_db.sqlite')
#engine = create_engine('sqlite:///w_db.sqlite')
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class TblHosts(Base):
    __tablename__ = 'Tbl_hosts'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    host_name = Column(String(150))
    host_comment = Column(String(150))

    def __init__(self,  name=None, host_name=None, host_comment=None):
        self.name = name
        self.host_name = host_name
        self.host_comment = host_comment

    def __repr__(self):
        return '<hosts {} {} {} >'.format(self.name, self.host_name, self.host_comment)


class TblSettings(Base):
    __tablename__ = 'Tbl_settings'
    id = Column(Integer, primary_key=True)
    path_to = Column(String(150))
    type_path = Column(String(150))

    def __init__(self, path_to=None, type_path=None):
        self.path_to = path_to
        self.type_path = type_path


    def __repr__(self):
        return '<settings {} {}  >'.format(self.path_to, self.type_path)


class TblFilesForCopy(Base):
    __tablename__ = 'Tbl_files_for_copy'
    id = Column(Integer, primary_key=True)

    files_nam = Column(String(150))
    status_copy = Column(Boolean())

    def __init__(self, files_nam=None, status_copy = 0):
        self.files_nam = files_nam
        self.status_copy = status_copy

    def __repr__(self):
        return '<files_for_copy {} {} >'.format(self.files_nam, self.status_copy)


def create_DB():
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    # Создает базу данных
    Base.metadata.create_all(bind=engine)
