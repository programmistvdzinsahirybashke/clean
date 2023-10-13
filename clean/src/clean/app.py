"""
clean app
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import psycopg2 as db


def greeting(name):
    if name:
        return f"Hello, {name}"
    else:
        return "Hello, stranger"

class clean(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        try:
            # пытаемся подключиться к базе данных
            conn = db.connect(dbname='postgres', user='postgres', password='123', host='localhost')
            print('Established connection to database')
        except Exception as e:
            # в случае сбоя подключения будет выведено сообщение в STDOUT
            print(e)
            print('Can`t establish connection to database')

        main_box = toga.Box(style=Pack(direction=COLUMN))

        name_label = toga.Label(
            "Your name: ",
            style=Pack(padding=(0, 5))
        )
        self.name_input = toga.TextInput(style=Pack(flex=1))

        name_box = toga.Box(style=Pack(direction=ROW, padding=5))
        name_box.add(name_label)
        name_box.add(self.name_input)

        button = toga.Button(
            "Добавить в базу",
            on_press=self.say_hello,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def say_hello(self, widget):
        address = self.address_input.value



def main():
    return clean()
