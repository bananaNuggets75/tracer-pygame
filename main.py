import kivy
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line
from kivy.uix.label import Label
from kivy.core.window import Window

patterns = [
    [(100, 100), (300, 300), (500, 100)],
    [(200, 400), (200, 200), (400, 200), (400, 400)],
]

class TraceGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pattern_order = list(range(len(patterns)))
        random.shuffle(self.pattern_order)
        self.current_pattern_index = 0
        self.current_pattern = self.pattern_order[self.current_pattern_index]
        self.score = 0
        
        # Define the score_label attribute
        self.score_label = Label(text="Score: 0", pos=(10, Window.height - 60), font_size=30)
        self.add_widget(self.score_label)  # Add the label widget to the game
        
        self.draw_pattern()

    def draw_pattern(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0)
            self.pattern_line = Line(points=[coord for point in patterns[self.current_pattern] for coord in point], width=2)

    def next_pattern(self):
        self.current_pattern_index += 1
        if self.current_pattern_index < len(self.pattern_order):
            self.current_pattern = self.pattern_order[self.current_pattern_index]
            self.draw_pattern()
        else:
            self.canvas.clear()
            with self.canvas:
                Color(0, 1, 0)
                self.add_widget(Label(text="Game Over!", font_size=50, center=self.center))

    def on_touch_down(self, touch):
        next_point = patterns[self.current_pattern][0]
        if (next_point[0] - 20 < touch.x < next_point[0] + 20) and (next_point[1] - 20 < touch.y < next_point[1] + 20):
            patterns[self.current_pattern].pop(0)
            self.pattern_line.points = [coord for point in patterns[self.current_pattern] for coord in point]
            self.score += 10  # Increment score for correct trace
            self.update_score()

            if not patterns[self.current_pattern]:
                self.next_pattern()  # Call the method to update to the next pattern

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"

class TraceApp(App):
    title = 'Trace the Path'

    def build(self):
        return TraceGame()

if __name__ == '__main__':
    TraceApp().run()
