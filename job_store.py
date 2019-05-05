#!/user/bin/env python
# -*- coding:utf-8 -*-


import datetime
import uuid as ud

from sqlalchemy import Column, String, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/DB1', echo=True)
session = sessionmaker(bind=engine)()


def init_md_job_store(cls):
    Base.metadata.create_all(engine)
    return 1


def clean_md_job_store(cls):
    Base.metadata.drop_all(engine)
    return 1


class Jobs(Base):
    __tablename__= 'JOBS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String(50), nullable=False)
    uuid = Column(String(36), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    version = Column(Integer)
    category = Column(String(50))
    priority = Column(Integer)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    delete_date = Column(DateTime)

    def __init__(self, name, state, uuid, version, category, priority, create_date, update_date, delete_date):
        self.name = name
        self.state = state
        self.uuid = uuid
        self.version = version
        self.category = category
        self.priority = priority
        self.create_date = create_date
        self.update_date = update_date
        self.delete_date = delete_date

    def __repr__(self):
        return ("name=\'%s\', state=\'%s\', uuid=\'%s\', version=%s, category=\'%s\', priority=\'%s\', "
                "create_date=%s, update_date=%s, delete_date=%s"
                % (self.name, self.state, self.uuid, self.version, self.category, self.priority, self.create_date, self.update_date, self.delete_date))

    @classmethod
    def create_jobs(cls, name, category, priority):
        name = name
        state = 'disabled'
        uuid = str(ud.uuid1())
        version = 0
        category = category
        priority = priority
        create_date = datetime.datetime.now()
        update_date = datetime.datetime.now()
        delete_date = None
        job = cls(name, state, uuid, version, category, priority, create_date, update_date, delete_date)
        session.add(job)
        session.commit()
        return 1

    @classmethod
    def get_jobs_by_job_name(cls, name):
        for instance in session.query(Jobs).filter_by(name=name):
            return instance

    @classmethod
    def get_jobs_by_category(cls, category):
        if isinstance('str', str):
            return session.query(Jobs).filter(Jobs.category == category)
        elif isinstance('str', list):
            return session.query(Jobs).filter(Jobs.category.in_(category))


class Transforms(Base):
    __tablename__ = 'JOB_TRANSFORMS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True)
    state = Column(String(50), nullable=False)
    job_uuid = Column(String(36), unique=True)
    script_type = Column(String(50), nullable=False)
    out_type = Column(String(50), nullable=False)
    source_name = Column(String(50), nullable=False)
    target_type = Column(String(50), nullable=False)
    target_name = Column(String(50), nullable=False)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    delete_date = Column(DateTime)

    def __init__(self, state, job_uuid, script_type, source_type, source_name, target_type, target_name, create_date, update_date, delete_date):
        self.state = state
        self.job_uuid = job_uuid
        self.script_type = script_type
        self.source_type = source_type
        self.source_name = source_name
        self.target_type = target_type
        self.target_name = target_name
        self.create_date = create_date
        self.update_date = update_date
        self.delete_date = delete_date

    def __repr__(self):
        return ("job_uuid = %s, state = %s, script_type = %s, source_type=%s, source_name = %s,"
                "target_type = %s, target_name = %s,create_date = %s, update_date = %s, delete_date = %s"
                % (self.job_uuid, self.state, self.script_type, self.source_type, self.target_type, self.target_name, self.create_date, self.update_date, self.delete_date))

    @classmethod
    def create_transform(cls, script_type, source_type, source_name, target_type, target_name):
        uuid = str(ud.uuid1())
        state = 'inactive'
        job_uuid = None
        create_date = datetime.datetime.now()
        update_date = datetime.datetime.now()
        delete_date = None
        transform = cls(uuid,state,job_uuid, script_type,source_type,source_name,target_type,target_name,create_date, update_date, delete_date)
        session.add(transform)
        session.commit
        return transform

    @staticmethod
    def get_transform_by_uuid(self, uuid):
        return session.query(Transforms).filter(Transforms.uuid == uuid)

    def is_linked(self):
        if self.job_uuid is not None:
            return True
        else:
            return False

    def link_job_transform(self,job_uuid):
        if self.is_linked():
            return 0
        else:
            self.job_uuid =job_uuid
            session.commit()
        return 1


class Conditions(Base):
    __tablename__ = 'JOB_CONDITIONS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=False, unique=True)
    state = Column(String(50), nullable=False)
    job_uuid = Column(String(36), unique=True)
    condition_type = Column(String(50), nullable=False)
    condition_job = Column(String(36))
    condition_start = Column(String(20))
    condition_end = Column(String(20))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    delete_date = Column(DateTime)

    def create_job_conditions(object):
        pass


Jobs.clean_md_job_store()
Jobs.init_md_job_store()
Jobs.create_jobs('IMP_UIBS_T1_FULL', 'UIBS', 2)
Transforms.create_job_details('kettle', 'oracle', 'uibs', 'trafodion', 'traf')


#Jobs.create_jobs('IMP_UIBS_T2_FULL', 'U1', 2)
#Jobs.create_jobs('IMP_UIBS_T3_FULL', 'U1', 3)
#Jobs.create_jobs('IMP_UIBS_T4_FULL', 'U1', 3)
#print(Jobs.get_jobs_by_job_name('IMP_U1_T4_FULL'))









