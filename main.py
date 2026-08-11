
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.utils import get_color_from_hex
from kivy.core.window import Window


class PaintWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_color = get_color_from_hex("#E81C1D") # Красный по умолчанию
        self.line_width = 2
        self.history = []  # История штрихов для отмены
        self.current_line = None

        # Задаем белый фон холста
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, instance, value):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.current_color)
                # Начинаем новую линию
                self.current_line = Line(points=(touch.x, touch.y), width=self.line_width)
                self.history.append(self.current_line)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos) and self.current_line:
            self.current_line.points += [touch.x, touch.y]
            return True
        return super().on_touch_move(touch)

    def clear_canvas(self):
        self.canvas.clear()
        self.history.clear()
        # Восстанавливаем белый фон
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

    def undo(self):
        if self.history:
            last_line = self.history.pop()
            self.canvas.remove(last_line)


class PyPainterApp(App):
    def build(self):
        self.painter = PaintWidget()

        # Главный контейнер
        main_layout = BoxLayout(orientation='vertical')

        # 1. Верхняя панель (Отмена и Очистка)
        top_panel = BoxLayout(size_hint_y=0.08, padding=5, spacing=5)
        
        btn_undo = Button(text="Отмена ↩️", background_color=get_color_from_hex("#FF9800"))
        btn_undo.bind(on_release=lambda x: self.painter.undo())
        
        btn_clear = Button(text="Очистить 🗑️", background_color=get_color_from_hex("#E81C1D"))
        btn_clear.bind(on_release=lambda x: self.painter.clear_canvas())
        
        top_panel.add_widget(btn_undo)
        top_panel.add_widget(btn_clear)

        # 2. Холст для рисования
        main_layout.add_widget(top_panel)
        main_layout.add_widget(self.painter)

        # 3. Нижняя панель с выбором цвета и размера
        bottom_panel = BoxLayout(orientation='vertical', size_hint_y=0.25, padding=5, spacing=5)

        # Слайдер толщины
        slider = Slider(min=1, max=50, value=2, size_hint_y=0.3)
        slider.bind(value=self.on_slider_change)

        # Палитра цветов (2 строки кнопок)
        palette = GridLayout(rows=2, cols=7, spacing=3)

        colors = [
            ("красный", "#E81C1D"), ("оранжевый", "#FF7F00"), ("жёлтый", "#FDE005"),
            ("зелёный", "#38B615"), ("салатовый", "#7CFC00"), ("голубой", "#1AC5EB"), ("синий", "#221CE8"),
            ("фиолетовый", "#8D1AEB"), ("розовый", "#FF69B4"), ("древесный", "#8B5A2B"),
            ("серый", "#808080"), ("чёрный", "#000000"), ("Ластик", "#FFFFFF")
        ]

        for name, hex_code in colors:
            btn = Button(text=name, font_size='11sp')
            btn.color = (0, 0, 0, 1) if hex_code in ["#FFFFFF", "#FDE005", "#7CFC00"] else (1, 1, 1, 1)
            btn.background_color = get_color_from_hex(hex_code)
            btn.bind(on_release=lambda instance, code=hex_code: self.set_color(code))
            palette.add_widget(btn)

        bottom_panel.add_widget(slider)
        bottom_panel.add_widget(palette)

        main_layout.add_widget(bottom_panel)
        return main_layout

    def set_color(self, hex_code):
        self.painter.current_color = get_color_from_hex(hex_code)

    def on_slider_change(self, instance, value):
        self.painter.line_width = value


if __name__ == '__main__':
    PyPainterApp().run()
