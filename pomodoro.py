"""
MIT License

Copyright (c) 2020 Patrick Palma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import tm1637

DIO = 0
CLK = 1


class Pomodoro:
    def __init__(self, tm_instance, sessions=4, work_time=25, pause_time=5, last_pause_time=15):
        self.tm = tm_instance
        self.sessions = sessions
        self.work_time = work_time
        self.pause_time = pause_time
        self.last_pause_time = last_pause_time
        self.tm.scroll('pomodoro', 200)

    def _countdown(self, minutes):
        for minute in range(minutes - 1, -1, -1):
            for second in range(59, -1, -1):
                self.tm.numbers(minute, second)
                time.sleep(1)

    def _pomodoro(self, current_session):
        self.tm.scroll('STARTING SESSION %d of %d' % (current_session, self.sessions))
        self._countdown(self.work_time)

    def _pause(self, minutes):
        self.tm.scroll('PAUSE STARTED')
        self._countdown(minutes)
        self.tm.scroll('PAUSE FINISHED')

    def run(self):
        for i in range(1, self.sessions + 1):
            self._pomodoro(i)

            pause_time = self.pause_time if self.sessions > i else self.last_pause_time
            self._pause(pause_time)

        self.tm.scroll('POMODORO FINISHED')


if __name__ == '__main__':
    tm = tm1637.TM1637(dio=DIO, clk=CLK, brightness=2)
    pomodoro = Pomodoro(tm, 2)
    pomodoro.run()
