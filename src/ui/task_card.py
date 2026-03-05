import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.models.repositories.subtasks_repository import SubTaskRepository
from src.ui.task_progress import TaskProgress

class TaskCard(Gtk.Box):
    def __init__(self, task, percentage,  callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.get_style_context().add_class("card-tasks")
        self.callback = callback
        self.task = task

        title_label = Gtk.Label(label=task.name)
        title_label.set_markup(f'<b>{task.name}</b>')

        percentage_progress = Gtk.ProgressBar()
        percentage_progress.set_fraction(percentage / 100.0)
        percentage_progress.set_show_text(f"{percentage}%")
        percentage_progress.add_css_class("custom-progress")

        

        action_button = Gtk.Button(label="Acompanhar")
        action_button.connect("clicked", self.on_click)

        self.append(title_label)
        self.append(percentage_progress)
        self.append(action_button)

    def on_click(self, button):
        self.callback(self.task)

   
