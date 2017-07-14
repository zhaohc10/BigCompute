# -*- coding: utf-8 -*-


import luigi
import random,time

class WordPicker(luigi.Task):
    def output(self):
        return luigi.LocalTarget('./output/word-picker/word.txt')

    def run(self):
        words = ["purple", "blue", "tooth", "beachball"]
        index = random.randint(0,3)
        chosen_word = words[index]

        with self.output().open('w') as f:
            f.write(chosen_word)

class FlipWordBackwards(luigi.Task):
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