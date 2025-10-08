from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle

from muscle_logic import Liste_muscles, set_muscle_goal


class MuscleCard(BoxLayout):
    """
    Carte stylisée : image + nom + boutons avec design arrondi et dégradé doux
    """
    def __init__(self, name, path, on_select, **kwargs):
        super().__init__(orientation="vertical",
                         padding=dp(15),
                         spacing=dp(15),
                         **kwargs)
        
        self.name = name
        self.path = path
        self.on_select = on_select

        # --- fond arrondi / couleur ---
        with self.canvas.before:
            Color(0.1, 0.1, 0.15, 1)  # gris foncé bleuté
            self.bg = RoundedRectangle(radius=[dp(20)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        # --- image ---
        if path:
            self.add_widget(Image(source=path, allow_stretch=True, keep_ratio=True, size_hint_y=0.6))
        else:
            self.add_widget(Label(text="[Image manquante]", markup=True, font_size="16sp"))

        # --- nom du muscle ---
        self.add_widget(Label(text=name.upper(),
                              bold=True,
                              font_size="24sp",
                              color=(1, 1, 1, 1),
                              size_hint_y=None,
                              height=dp(40)))

        # --- boutons ---
        btn_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))

        buttons = [
            ("Maintenance", (0.8, 0.8, 0.8, 1), "maintenance"),
            ("Normal", (0.4, 0.6, 1, 1), "normal_growth"),
            ("Priorité", (1, 0.4, 0.4, 1), "prioritised_growth"),
        ]

        for text, color, goal in buttons:
            btn = StyledButton(text=text, bg_color=color)
            btn.bind(on_press=lambda instance, g=goal: self.on_select(name, g))
            btn_row.add_widget(btn)

        self.add_widget(btn_row)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class StyledButton(Button):
    """
    Boutons arrondis et colorés pour un look plus moderne
    """
    def __init__(self, bg_color=(0.5, 0.5, 0.5, 1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.color = (1, 1, 1, 1)
        self.font_size = "18sp"
        self.bold = True
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(15)])


class MuscleScreen(BoxLayout):
    """
    Version moderne : un muscle à la fois avec transitions douces
    """
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(20), spacing=dp(20), **kwargs)
        self.current_index = 0
        self.muscles = Liste_muscles
        self.card = None
        self.display_current_muscle()

    def display_current_muscle(self):
        self.clear_widgets()

        if self.current_index >= len(self.muscles):
            self.add_widget(Label(text=" Sélection terminée :)) !",
                                  font_size="28sp",
                                  bold=True,
                                  color=(1, 1, 1, 1)))
            return

        name, path = self.muscles[self.current_index]
        self.card = MuscleCard(name, path, self.select_goal)
        self.add_widget(Widget(size_hint_y=None, height=dp(40)))  # petit espace haut
        self.add_widget(self.card)

        # effet d'apparition douce
        self.card.opacity = 0
        Animation(opacity=1, d=0.3).start(self.card)

    def select_goal(self, muscle_name, goal):
        set_muscle_goal(muscle_name, goal)
        self.current_index += 1
        self.display_current_muscle()

if __name__ == "__main__":
    from kivy.app import App

    class _DemoApp(App):
        def build(self):
            return MuscleScreen()

    _DemoApp().run()