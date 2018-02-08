import curses
import atexit

initialized = False
stdscr = None
def init():
    global stdscr, initialized
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    initialized = True

@atexit.register
def quit():
    global stdscr, initialized
    if not initialized:
        return
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    initialized = False
    
class UI:
    def __init__(self):
        if not initialized:
            init()
        self.win = curses.newwin(curses.LINES-1, curses.COLS-1)

    def update(self, lines):
        self.win.clear()
        for i in range(len(lines)):
            self.win.addstr(i, 0, lines[i])
        self.win.refresh()


if __name__ == '__main__':
    import time
    from datetime import datetime
    ui = UI()
    while True:
        try:
            lines = ('this is the first line',
                     'this is the second line',
                     'clock: %s' % datetime.now())
            ui.update(lines)
            time.sleep(1)
        except KeyboardInterrupt:
            break
