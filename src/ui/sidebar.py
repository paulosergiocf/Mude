
import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk

class Sidebar(Gtk.Box):
    LEN_SIDEBAR = 250
    def __init__(self, task_all, tasks_week, quit_app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_name("sidebar")
        self.set_size_request(self.LEN_SIDEBAR, -1)

        tasks = Gtk.Button(label="Tasks")
        week = Gtk.Button(label="Week")
        sair = Gtk.Button(label="Quit")

        tasks.connect("clicked", task_all)
        week.connect("clicked", tasks_week)
        sair.connect("clicked", quit_app)

        self.append(tasks)
        self.append(week)
        self.append(sair)


