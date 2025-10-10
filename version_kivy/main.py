from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from muscle_screen import MuscleScreen

class MainApp(App):
    # méthode qui retourne le widget racine
    def build(self):
        # formzt téléphone vertical, aucun effet sur android
        Window.size = (450, 800)
                            #r g b alpha = transparence
        Window.clearcolor = (0.07, 0.07, 0.1, 1)

        screen = MuscleScreen()
        return screen

if __name__=="__main__":
    MainApp().run()
        

