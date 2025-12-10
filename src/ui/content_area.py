
import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.ui.task_card import TaskCard
from src.ui.task_progress import TaskProgress
from src.ui.task_crud import TaskCrud
from src.ui.subtasks_day import SubtasksDay
from src.models.repositories.tasks_repository import TaskRepository
from src.models.repositories.subtasks_repository import SubTaskRepository

class ContentArea(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_name("content-area")
        self.set_hexpand(True)
        self.set_vexpand(True)
        self.setup_scrolled_window()
        self.task_all()
    
    def task_all(self):
        self.clear_content()
        tasks = TaskRepository.get_all()
        add_task = Gtk.Button(label="Adicionar Task")
        add_task.connect("clicked", self.create_task)

        self.content_box.append(add_task)

        for task in tasks:
            percentage = SubTaskRepository.get_percentage_task(task)
            self.content_box.append(TaskCard(task=task, percentage=percentage, callback=lambda t: self.task_view(t)))

    def task_view(self, task=None):
        self.clear_content()
        percentage = SubTaskRepository.get_percentage_task(task)
        task_progress = TaskProgress(task=task,percentage=percentage, callback=self.task_all)
        self.content_box.append(task_progress)


    def create_task(self, button):
        self.clear_content()
        self.content_box.append(TaskCrud(callback=self.task_all))


    def task_week(self):
        self.clear_content()
        tasks = TaskRepository.get_all()
        days = SubTaskRepository.list_week(tasks)
        self.content_box.append(SubtasksDay(days=days, callback=self.task_week))

    def clear_content(self):
        while self.get_first_child() is not None:
            child = self.get_first_child()
            self.remove(child)

        self.setup_scrolled_window()

    def setup_scrolled_window(self):
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        self.scrolled_window.set_hexpand(True)
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scrolled_window.set_child(self.content_box)
        self.append(self.scrolled_window)