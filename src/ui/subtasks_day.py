import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.models.repositories.tasks_repository import TaskRepository
from src.models.repositories.subtasks_repository import SubTaskRepository
from src.ui.subtask_crud import SubTaskCrud
from src.ui.subtask_item import SubtasksItem

class SubtasksDay(Gtk.Box):
    
    def __init__(self, days = None, callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.get_style_context().add_class("card-subtasks-day")
        self.setup_scrolled_window()
        self.callback = callback

        for day, subtasks in days.items():
            container_item = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            container_item.get_style_context().add_class("subtask-item")
            title_week = Gtk.Label(label="")
            title_week.set_markup(f'<b>{day}</b>')
            container_item.append(title_week)
            subtasks_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            subtasks_container.set_margin_start(15)
            
            for subtask in subtasks:
                subtasks_container.append(SubtasksItem(subtask=subtask, callback=self.callback, main=self))
            
            container_item.append(subtasks_container)

            self.content_box.append(container_item)
 

    def clear_content(self):
        while self.get_first_child() is not None:
            child = self.get_first_child()
            self.remove(child)

        self.setup_scrolled_window()

    def setup_scrolled_window(self):
        """Configura a janela de rolagem e a caixa de conteúdo."""
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        self.scrolled_window.set_hexpand(True)

        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scrolled_window.set_child(self.content_box)

        self.append(self.scrolled_window)
        