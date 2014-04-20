#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright © 2014 Tim Bielawa <timbielawa@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import json
from pprint import pprint as pp
import datetime
import calendar

CONFIG = {}

def get_config():
    config_locations = [".paydisplay.json", "paydisplay.json", os.path.expanduser("~/.paydisplay.json")]

    for location in config_locations:
        if os.path.exists(location):
            c = json.loads(open('paydisplay.json', 'r').read())
            break

    global CONFIG
    CONFIG = c
    return c

def disp(item):
    _prefix = colorize('white', 'Displaying: ')
    _item = colorize('red', item)
    print "%s%s" % (_prefix, _item)

def colorize(color, item):
    COLORS = {}
    COLORS['RESTORE'] = '\033[0m'
    COLORS['RED'] = '\033[00;31m'
    COLORS['GREEN'] = '\033[00;32m'
    COLORS['YELLOW'] = '\033[00;33m'
    COLORS['BLUE'] = '\033[00;34m'
    COLORS['PURPLE'] = '\033[00;35m'
    COLORS['CYAN'] = '\033[00;36m'
    COLORS['LIGHTGRAY'] = '\033[00;37m'
    COLORS['LRED'] = '\033[01;31m'
    COLORS['LGREEN'] = '\033[01;32m'
    COLORS['LYELLOW'] = '\033[01;33m'
    COLORS['LBLUE'] = '\033[01;34m'
    COLORS['LPURPLE'] = '\033[01;35m'
    COLORS['LCYAN'] = '\033[01;36m'
    COLORS['WHITE'] = '\033[01;37m'
    # restore, set color, item text, restore
    return "%s%s%s%s" % (COLORS['RESTORE'],
                         COLORS[color.upper()],
                         item,
                         COLORS['RESTORE'])

def help():
    print """
d|display - display calendar
c|config - display config
h|help - help
q|quit - quit"""

def repl():
    print colorize('yellow', "Enter 'h' or 'help' to see commands available")
    while True:
        #display_calendar()
        #sys.exit(0)
        cmd = raw_input('command: ')
        if cmd == 'd' or cmd == 'disp':
            disp('Calendar')
            display_calendar()
        elif cmd == 'c' or cmd == 'config':
            disp('Config')
            display_config()
        elif cmd == 'q' or cmd == 'quit':
            disp('QUIT')
            break
        else:
            disp('HELP')
            help()


    sys.exit(0)

def display_config():
    print(json.dumps(CONFIG, indent=4))


def display_week(day, color_day=None):
    # By default, colorize 'today' in the week. But if 'color_day' is
    # given, only colorize days that match 'color_day'. If no days
    # match, nothing is colored.
    if not color_day:
        color_day = day

    if day.weekday() == 6:
        dow = 0
    else:
        # The +1 accounts for days starting on monday
        dow = day.isoweekday()
    #disp('Weekday: %s' % colorize('green', dow))
    one_day = datetime.timedelta(days=1)

    # Weeks start on sunday
    sunday = day - (one_day * dow)
    # Collect the items to print for this week
    week_days = []

    for i in xrange(7):
        day_to_show = sunday + (one_day * i)
        if day_to_show.day == color_day.day:
            week_days.append(colorize('PURPLE', str(day_to_show.day).zfill(2)))
        else:
            if day_to_show.month != color_day.month:
                week_days.append(colorize('lightgray', str(day_to_show.day).zfill(2)))
            else:
                week_days.append(colorize('white', str(day_to_show.day).zfill(2)))

    print " %s  %s  %s  %s  %s  %s  %s " % tuple(map(lambda x: str(x).zfill(2), week_days))


def display_month(start_day):
    # Get the first day of the month by finding what the current day
    # is. Get this from day.day.
    day = datetime.timedelta(days=1)
    #first_day = start_day - (day * (start_day.day - 1))
    first_day = datetime.datetime(start_day.year, start_day.month, 1)
    days_in_month = calendar.monthrange(start_day.year, start_day.month)[1]
    # Then make a new day that is today - day * todays number
    #display_week(first_day, color_day=start_day)
    i = 0
    #disp("Start day: %s" % colorize('green', str(start_day)))
    #disp("First day: %s" % colorize('green', str(first_day)))
    while i < days_in_month:
        day_diff = (day * i)
        #print day_diff
        display_week(first_day + day_diff, color_day=start_day)
        i += 7

def display_year(day):
    pass

def display_calendar():
    # First, display today
    today = datetime.datetime.now()
    disp('Today: %s' % colorize('yellow', today.day))
    # Then display this week
    display_week(today)
    # Then display this month
    disp("Month")
    display_month(today)
    # Then display this year
    disp("Year")
    display_year(today)

def main():
    get_config()
    result = repl()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt, e:
        pass

    #     print e
    #     import pdb
    #     pdb.set_trace()
