from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App
from kivy.core.window import Window
from kivy.cache import Cache
from kivy.clock import Clock

from exercise_database import get_exercises_by_pattern
from exercise_database import EXERCISE_DATABASE


def get_all_patterns():
    return sorted(list({info["pattern"] for info in EXERCISE_DATABASE.values()}))

# hérite de ButtonBehavior et de BoxLayout
class ExerciseCard(ButtonBehavior, BoxLayout):
    # constructeur de la classe
    def __init__(self, name, image_path, on_click, **kwargs):
        super().__init__(orientation="vertical",
                         padding=dp(8),
                         spacing=dp(4),
                         size_hint_y=None,
                         height=dp(220),
                         **kwargs)

        self.name = name
        self.image_path = image_path
        self.on_click = on_click

        # before = arrière plan 
        with self.canvas.before:       # dp c'est density independent pixel
            Color(0.1, 0.1, 0.15, 1)   # radius du coin arrondi
            self.bg = RoundedRectangle(radius=[dp(15)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        img_path = EXERCISE_DATABASE[name].get("image_path", "")
        print(f"[DEBUG] Exercise: {name}, Image path: {img_path}")
        
        if img_path:
            # Vérifier si le fichier existe
            import os
            if os.path.exists(img_path):
                print(f"[DEBUG] Image file exists for {name}")
                try:
                    # Nettoyer le cache pour cette image en particulier
                    Cache.remove('kv.texture', img_path)
                    Cache.remove('kv.image', img_path)
                    
                    # Créer l'image avec gestion d'erreur
                    image_widget = Image(
                        source=img_path,
                        allow_stretch=True,
                        keep_ratio=True,
                        size_hint_y=0.8
                    )
                    
                    # Attendre un peu pour le chargement asynchrone
                    def check_texture(widget, *args):
                        if widget.texture is None:
                            print(f"[DEBUG] Image texture still None for {name} after delay")
                            # Retirer l'image défaillante et ajouter un label d'erreur
                            if widget.parent:
                                widget.parent.remove_widget(widget)
                                widget.parent.add_widget(Label(
                                    text="(erreur texture)",
                                    font_size="14sp",
                                    color=(1, 0.7, 0, 1),
                                    size_hint_y=0.8
                                ))
                        else:
                            print(f"[DEBUG] Image texture loaded successfully for {name}")
                    
                    # Vérifier la texture après un court délai
                    Clock.schedule_once(lambda dt: check_texture(image_widget), 0.1)
                    
                    self.add_widget(image_widget)
                except Exception as e:
                    print(f"[DEBUG] Image loading error for {name}: {e}")
                    self.add_widget(Label(
                        text="(erreur chargement)",
                        font_size="14sp",
                        color=(1, 0.7, 0, 1),  # Orange pour erreur de chargement
                        size_hint_y=0.8
                    ))
            else:
                print(f"[DEBUG] Image file MISSING for {name}: {img_path}")
                self.add_widget(Label(
                    text="(image manquante)",
                    font_size="14sp",
                    color=(1, 0.5, 0.5, 1),  # Rouge clair pour les images manquantes
                    size_hint_y=0.8
                ))
        else:
            print(f"[DEBUG] No image path defined for {name}")
            self.add_widget(Label(
                text="(pas d'image)",
                font_size="14sp",
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=0.8
            ))

        
        self.add_widget(Label(
            text=name,
            font_size="16sp",
            bold=True,
            color=(1,1,1,1),
            halign="center",
            valign="middle",
            size_hint_y=0.2
        ))
    
    # pour que le widget suive l'image si jamais elle change de position
    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_press(self):
        self.on_click(self.name)

class ExerciseScreen(ScrollView):

    def __init__(self, pattern_name, on_pattern_finished, **kwargs):
        super().__init__(**kwargs)
        self.pattern_name = pattern_name
        self.on_pattern_finished = on_pattern_finished
        self.selected_count = 0

        grid = GridLayout(cols=2, spacing=dp(12), padding=dp(12), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        exercices = get_exercises_by_pattern(pattern_name)

        for name in exercices:
            info = EXERCISE_DATABASE.get(name, {})
            image_path = info.get("image_path", "")
            card = ExerciseCard(name, image_path, on_click=self.on_exercise_selected)
            grid.add_widget(card)

        self.add_widget(grid)

    def on_exercise_selected(self, exercise_name):
        self.selected_count += 1

        if self.selected_count >= 2:
            self.on_pattern_finished()
        
class PatternFlowApp(App):
    def build(self):
        # Window.size = (480, 820)
        self.patterns = get_all_patterns()
        self.current_index = 0
        return self.load_next_pattern()

    def load_next_pattern(self):
        if self.current_index >= len(self.patterns):
            return Label(text="Séléction terminée", font_size="20sp")

        pattern_name = self.patterns[self.current_index]
        self.current_index += 1

        return ExerciseScreen(
            pattern_name=pattern_name, 
            on_pattern_finished=self.next_pattern
            
        )
    
    def next_pattern(self):
        self.root.clear_widgets()
        next_screen = self.load_next_pattern()
        self.root.add_widget(next_screen)


if __name__ == "__main__":
    PatternFlowApp().run()



