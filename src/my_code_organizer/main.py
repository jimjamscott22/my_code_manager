import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw
from .window import MainWindow
from .models.database import get_db

class MyCodeOrganizerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.github.mycode.organizer')

    def do_activate(self):
        # Initialize database
        db = get_db()
        db.connect()

        # Create and show window
        win = MainWindow(self)
        win.present()

    def do_shutdown(self):
        # Close database connection
        db = get_db()
        db.close()

def main():
    app = MyCodeOrganizerApp()
    return app.run(sys.argv)

if __name__ == '__main__':
    main()
