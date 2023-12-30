from kivy.config import Config


Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    V_NB_LINES = 10
    V_LINES_SPACING = .25 #pourcentage sur la largeur de l'écran
    vertical_lines = []

    H_NB_LINES = 8
    H_LINES_SPACING = .1  # pourcentage sur la largeur de l'écran
    horizontal_lines = []
    SPEED = 2
    current_offset_y = 0

    SPEED_X = 12
    current_speed_x = 0
    current_offset_x = 0
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
       # print("INIT W:" + str(self.width) + " H:" + str(self.height))
        self.init_vertical_lines()
        self.init_horizontal_lines()

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard = None


    
    def on_parent(self, widget, parent):
        print("ON PARENT W:" + str(self.width) + " H:" + str(self.height))


    def on_size(self, *args):
        #self.update_vertical_lines()
        #self.update_horizontal_lines()
        pass
        #print("ON SIZE W:" + str(self.width) + " H:" + str(self.height))
        #self.perspective_point_x = self.width / 2
        #self.perspective_point_y = self.height * 0.75

    def on_perspective_point_x(self, widget, value):
        pass
        #print("PX: " + str(value))

    def on_perspective_point_y(self, widget, value):
        pass
        #print("PY: " + str(value))

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range (0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        central_line_x = self.width / 2
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES / 2)+0.5
        for i in range(0, self.V_NB_LINES):
            line_x = int(central_line_x + offset * spacing + self.current_offset_x)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1
        #self.line.points = [self.perspective_point_x, 0, self.perspective_point_x, 100]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range (0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        central_line_x = self.width / 2
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES / 2) + 0.5

        xmin = central_line_x+offset*spacing + self.current_offset_x
        xmax = central_line_x-offset*spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height
        for i in range(0, self.H_NB_LINES):
            line_y = i* spacing_y - self.current_offset_y
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        return self.tranfsorm_perspective(x, y)
        #return self.tranfsorm_2D(x, y)



    def tranfsorm_2D(self, x, y):
        return int(x), int(y)

    def tranfsorm_perspective(self, x, y):
        #TO DO
        lin_y = y * self.perspective_point_y / self.height
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x-self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = diff_y / self.perspective_point_y
        factor_y = pow(factor_y, 4)

        offset_x = diff_x *  factor_y

        tr_x = self.perspective_point_x + offset_x
        tr_y = self.perspective_point_y - factor_y*self.perspective_point_y
        return int(tr_x), int(tr_y)
    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = -self.SPEED_X
        return True


    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
    def on_touch_down(self, touch):
        if touch.x < self.width/2:
            print("<-")
            self.current_speed_x = self.SPEED_X
        else:
            print("->")
            self.current_speed_x = -self.SPEED_X


    def on_touch_up(self, touch):
        #print("UP")
        self.current_speed_x = 0

    def update(self, dt):
        #print("dt : " + str(dt*60))
        time_factor = dt*60
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.current_offset_y += self.SPEED * time_factor

        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y-=spacing_y

        self.current_offset_x += self.current_speed_x * time_factor





class GalaxyApp(App):
    pass


GalaxyApp().run()