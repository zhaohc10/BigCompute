# -*- coding: utf-8 -*-

import datetime
import logging
from contextlib import contextmanager

from luigi import six

from luigi import configuration
from luigi import task_history
from luigi.task_status import DONE, FAILED, PENDING, RUNNING

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.orm.collections
from sqlalchemy.engine import reflection
Base = sqlalchemy.ext.declarative.declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(20))



# db_connection = mysql://admin:lu1g1p4ss@mysql/luigid

config = configuration.get_config()
connection_string = config.get('task_history', 'db_connection')
self_engine = sqlalchemy.create_engine(connection_string)
self_session_factory = sqlalchemy.orm.sessionmaker(bind=self_engine, expire_on_commit=False)
Base.metadata.create_all(self_engine)

session = self_session_factory()
new_user = User(id='5', name='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()

# result = self_engine.execute('select * from tasks')
# res = result.fetchall()
# print(res)