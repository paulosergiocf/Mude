import sys
import gi
import os
from dotenv import load_dotenv
load_dotenv()

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.ui.content_area import ContentArea
from src.ui.sidebar import Sidebar
from src.util.config_util import ConfigUtil

class App(Gtk.Application):
    WIDTH = 1000
    HEIGHT = 800
    APPLICATION_NAME = "Mude"
    LOGO = "logo.png"
    FILE_CSS = "css/style.css"

    def __init__(self):
        super().__init__(application_id="br.com.paulosergiocf.TaskManager")
        GLib.set_application_name(self.APPLICATION_NAME)
        GLib.set_prgname("br.com.paulosergiocf.TaskManager")
        
    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self, title=self.APPLICATION_NAME)
        self.window.set_default_size(self.WIDTH, self.HEIGHT)
        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        icon_theme.add_search_path(self.LOGO)
        self.window.set_icon_name(self.APPLICATION_NAME)
    
        self.ui = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.sidebar = Sidebar(self.task_all, self.task_week, self.quit_app)
        self.content_area = ContentArea()
        self.ui.append(self.sidebar)
        self.ui.append(self.content_area)
        self.window.set_child(self.ui)
        self.config(self.FILE_CSS)
        self.window.present()

    def config(self, css_file):
        css_provider = Gtk.CssProvider()
        if os.path.exists(css_file):
            css_provider.load_from_path(css_file)
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER
            )
        else:
            raise ValueError(f"CSS file '{css_file}' not found.")

    def task_all(self, button):
        ConfigUtil.wait_timeout()
        self.content_area.task_all()

    def task_week(self, button):
        ConfigUtil.wait_timeout()
        self.content_area.task_week()
        
    def quit_app(self, button):
        self.quit()

if __name__=='__main__':
    try:
        app = App()
        exit_status = app.run(sys.argv)
        sys.exit(exit_status)
    except KeyboardInterrupt as exitKey:
        pass

