# -*- coding: utf-8 -*-

import luigi
import random,time,datetime
from luigi.db_task_history import DbTaskHistory, Base
import functools
import itertools
from luigi import six
from luigi import configuration
import luigi
import json
import sqlalchemy
from luigi.db_task_history import DbTaskHistory, Base
from luigi.task_register import load_task
from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, \
    desc, DateTime, orm,TypeDecorator, TEXT
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

from luigi import configuration

from luigi.db_task_history import TaskEvent,TaskParameter,TaskRecord
from luigi.task_status import PENDING
from luigi import task_history
import logging
logger = logging.getLogger('luigi-interface')

# https://gist.github.com/samuell/93cc7eb6803fa2790042



class with_config(object):
    """
    Decorator to override config settings for the length of a function.
    """

    def __init__(self, config, replace_sections=False):
        self.config = config
        self.replace_sections = replace_sections

    def _make_dict(self, old_dict):
        if self.replace_sections:
            old_dict.update(self.config)
            return old_dict

        def get_section(sec):
            old_sec = old_dict.get(sec, {})
            new_sec = self.config.get(sec, {})
            old_sec.update(new_sec)
            return old_sec

        all_sections = itertools.chain(old_dict.keys(), self.config.keys())
        return {sec: get_section(sec) for sec in all_sections}

    def __call__(self, fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            import luigi.configuration
            orig_conf = luigi.configuration.LuigiConfigParser.instance()
            new_conf = luigi.configuration.LuigiConfigParser()
            luigi.configuration.LuigiConfigParser._instance = new_conf
            orig_dict = {k: dict(orig_conf.items(k)) for k in orig_conf.sections()}
            new_dict = self._make_dict(orig_dict)
            for (section, settings) in six.iteritems(new_dict):
                new_conf.add_section(section)
                for (name, value) in six.iteritems(settings):
                    new_conf.set(section, name, value)
            try:
                return fun(*args, **kwargs)
            finally:
                luigi.configuration.LuigiConfigParser._instance = orig_conf
        return wrapper


class BNTaskTrack(Base):
    __tablename__ = 'task_track'

    id = Column(Integer, primary_key=True)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tasks.id'), index=True)
    # start_time = sqlalchemy.Column(sqlalchemy.TIMESTAMP, index=True, nullable=False)
    # duration = Column(Integer, primary_key=True)
    # task_res = sqlalchemy.Column(sqlalchemy.String(20)) # success or failure
    #
    # def __repr__(self):
    #     return "TaskEvent(task_id=%s, start_time=%s, duration=%s, task_res=%s" % \
    #            (self.task_id, self.start_time, self.duration, self.task_res )


class BNDDTaskHistory(DbTaskHistory):

    def task_track(self, task):
        self.bn_add_task_track(task.task_id, BNTaskTrack(task_id='check_check'))

    def bn_add_task_track(self, my_task_id, event):

        res = self.bn_find_or_create_task(my_task_id)
        print 'fffffffffffffff',my_task_id
        print 'ooooooooooooooo',event
        print 'llllllllllllll',list(res)


        # fffffffffffffff WordPicker__99914b932b
        # ooooooooooooooo <__main__.BNTaskTrack object at 0x7facb9718890>
        # llllllllllllll [((2L, 'WordPicker__99914b932b', 'WordPicker', '821511063af8'), <sqlalchemy.orm.session.Session object at 0x7facba7be510>)]

        # for (task_record, session) in self._find_or_create_task(task):
        #     task_record.events.append(event)

    def bn_find_or_create_task(self, my_task_id):
        with self._session() as session:
            if my_task_id is not None:
                task_record = session.execute('select * from tasks where task_id = :my_task_id',
                                              {'my_task_id':my_task_id}).fetchall() #.first()
                if not task_record:
                    raise Exception("Task with record_id, but no matching Task record!")
                yield (task_record, session)
            else:
                raise Exception("gggggggggggggggggg")
        # task.record_id = task_record.id



class TimeTaskMixin(object):
    '''
    A mixin that when added to a luigi task, will print out
    the tasks execution time to standard out, when the task is
    finished
    '''

    @with_config(dict(task_history=dict(db_connection=configuration.get_config().get('task_history', 'db_connection'))))
    @luigi.Task.event_handler(luigi.Event.START)
    def save_start_time(self):
        self.start_time = int(time.time() * 1000)
        self.history = BNDDTaskHistory()

        self.history.task_track(self)
        print('### TASK START TIME ###: %s, %s, hhhhhh %s' % (self.task_id, self.start_time,'ff'))
        # self.log("Dependency present. Starting task")

    @with_config(dict(task_history=dict(db_connection=configuration.get_config().get('task_history','db_connection'))))
    @luigi.Task.event_handler(luigi.Event.PROCESSING_TIME)
    def processing_time(self, processing_time):
        print('### PROCESSING TIME ###: %s, %s' % (self.task_id, processing_time))

    @luigi.Task.event_handler(luigi.Event.FAILURE)
    def send_failure_event(self, exception):
        pass

    @luigi.Task.event_handler(luigi.Event.SUCCESS)
    def send_success_event(self):
        pass


class WordPicker(luigi.Task,TimeTaskMixin):
    def output(self):
        return luigi.LocalTarget('./output/word-picker/word.txt')

    def run(self):
        words = ["purple", "blue", "tooth", "beachball"]
        index = random.randint(0,3)
        chosen_word = words[index]

        with self.output().open('w') as f:
            f.write(chosen_word)

class FlipWordBackwards(luigi.Task,TimeTaskMixin):
    def requires(self):
        return WordPicker()

    def output(self):
        return luigi.LocalTarget('./output/word-picker/reversed_word.txt')

    def run(self):
        print self.input()
        with self.input().open('r') as raw_word:
            word = raw_word.read()
        time.sleep(5)
        with self.output().open('w') as f:
            f.write('I just reversed {0}'.format(word[::-1]))

if __name__ == "__main__":
    luigi.run()