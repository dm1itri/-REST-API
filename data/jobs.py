# import datetime
from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Job(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    team_leader_id = Column(Integer, nullable=False)
    work_size = Column(Integer, nullable=False)
    collaborators = Column(String)
    is_finished = Column(Boolean, default=False)
    user_created = Column(Integer, ForeignKey("users.id"))
    user = orm.relation('User')
