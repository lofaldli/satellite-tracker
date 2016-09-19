import sys
import arrow
import pygame as pg

WHITE = (255,255,255)
GREY = (100,100,100)
GREY_TRANS = pg.Color(100,100,100,100)
BLACK = (0,0,0)

class GUI:
    def __init__(self, width=800, height=400, fps=10):
        self.size = (width,height)
        self.fps = fps

        pg.init()
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption('satellite tracker', 'st')
        self.font = pg.font.SysFont('sansserif', 15)
        self.clock = pg.time.Clock()
        self.data = []

    def set_background(self, filename):
        self.image = pg.image.load(filename)

    def draw_background(self):
        self.image = pg.transform.scale(self.image, self.size)
        self.screen.fill(WHITE)
        self.screen.blit(self.image, self.image.get_rect())

    def draw_data(self):
        for d in self.data:
            x = int(d['x']*self.size[0])
            y = int(d['y']*self.size[1])
            self.draw_point((x,y))
            self.draw_label(d['label'], (x+10,y+10))

    def draw_point(self, pos=(0,0)):
        x,y=pos
        rect = pg.Rect(x,y, 5, 5)
        self.screen.fill(WHITE, rect)

    def draw_label(self, text='', pos=(0,0)):
        x,y=pos
        label = self.font.render(text.strip(), 1, WHITE)

        self.screen.fill(GREY_TRANS, pg.Rect(x,y,label.get_rect().width,label.get_rect().height))
        self.screen.blit(label, pos)

    def draw_line(self, pos0, pos1, color=GREY):
        pg.draw.line(self.screen, color, pos0, pos1)

    def draw_clock(self):
        t = arrow.utcnow()
        self.draw_label(t.format('YYYY-MM-DD HH:mm:ss.S'), (0,0))

    def draw_fps(self):
        fps = self.clock.get_fps()
        self.draw_label('FPS: ' + str(int(fps)), (self.size[0]-40,0))

    def draw_grid(self):
        lats = (-60,-30,0,30,60)
        lons = (-150,-120,-90,-60,-30,0,30,60,90,120,150)

        for lat in lats:
            lat = self.size[1] * (90.0 - lat) / 180.0
            pos0 = (0, lat)
            pos1 = (self.size[0], lat)
            self.draw_line(pos0,pos1,GREY)

        for lon in lons:
            lon = self.size[0] * (lon + 180) / 360.0
            pos0 = (lon, 0)

            pos1 = (lon, self.size[1])
            self.draw_line(pos0,pos1,GREY)




    def update(self):
        self.draw_background()
        self.draw_grid()
        self.draw_clock()
        self.draw_fps()
        self.draw_data()

        pg.display.flip()
        self.clock.tick(self.fps)



    def main_loop(self,callback=None,run_once=False):

        while True:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit()

            if callback:
                self.data = callback()

            self.update()
            if run_once:
                sys.exit()





if __name__=='__main__':
    gui = GUI(800,400)
    gui.set_background('world_map.jpg')
    gui.main_loop()
