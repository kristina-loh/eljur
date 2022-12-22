from kivy.app import App
from kivy.uix.label import Label
import get_data, json

class MainApp(App):

    get_data.data_dump()

    def build(self):
        f = open("table.json", "r")
        mp = json.loads(f.read())

        txt = ' '.join(sum(get_data.table(mp), []))
        label = Label(text=txt)
        return label

if __name__=='__main__':
    app = MainApp()
    app.run()
