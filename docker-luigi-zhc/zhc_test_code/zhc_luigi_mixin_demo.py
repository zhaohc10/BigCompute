# -*- coding: utf-8 -*-

import luigi
import random,time
# https://gist.github.com/samuell/93cc7eb6803fa2790042


class TimeTaskMixin(object):
    '''
    A mixin that when added to a luigi task, will print out
    the tasks execution time to standard out, when the task is
    finished
    '''
    @luigi.Task.event_handler(luigi.Event.START)
    def save_start_time(self):
        self.start_time = int(time.time() * 1000)
        print('### TASK START TIME ###: %s, %s' % (self.task_id, self.start_time))
        # self.log("Dependency present. Starting task")

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