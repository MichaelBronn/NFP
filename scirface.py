from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout #пространство для структурированного расположения элементов внутри
from kivy.uix.gridlayout import GridLayout #таблично-блочная структура
from kivy.uix.layout import Layout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter

from kivy.config import Config

#Config.set('graphics', 'resizable', '0') #фиксация размеров окна
Config.set('graphics', 'height', '700') #высота
Config.set('graphics', 'width', '1000') #ширина
class MyApp(App):
    def build(self):
        #s = Scatter() #штука для работы двумя пальцами на экране (увеличение, перемещние, поворот и тд)
        gl = GridLayout(cols=3, padding=10, spacing=10)
        for i in range(12):
            gl.add_widget(Button(text=f'Button-{i+1}'))
        bl = BoxLayout(orientation='horizontal', padding=[10], spacing=100)
        #s.add_widget(bl)
        but = Button(text="Нажми на меня",
                      font_size=30,
                      on_press=self.btn_press,
                      background_normal = "", #так как цвета работают в режиме умножения это задаёт пустой начальный цвет (изначально серый)
                      background_color = [1,0.1,0.1,1])#процентное rgba
        bl.add_widget(but)
        bl.add_widget(Button(text = "random Button"))

        return gl

    def btn_press(self, instance): #instance - для измения параметров юнита вызвавшего функцию
        print("Ну нажал ты кнопку, и что?")
        instance.text = "Нажал, молодец"
        instance.background_color = [0.1,0.1,1,1]



if __name__ == "__main__":
    MyApp().run()