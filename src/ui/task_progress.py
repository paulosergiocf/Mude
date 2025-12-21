import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.models.repositories.tasks_repository import TaskRepository
from src.models.repositories.subtasks_repository import SubTaskRepository
from src.util.date_util import DateUtil
from src.ui.task_weeks import TaskWeeks
from src.ui.task_crud import TaskCrud
from src.ui.subtask_crud import SubTaskCrud
class TaskProgress(Gtk.Box):
    
    def __init__(self, task, percentage,  callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.get_style_context().add_class("card-task")
        self.callback  = callback
        self.set_hexpand(True)
        self.set_vexpand(True)

        week_label_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        name_label = Gtk.Label(label=task.name)
        name_label.set_markup(f'<b>{task.name}</b>')
        week_label_container.append(name_label)

        description_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        description_label = Gtk.Label(label=f"{task.description}")
        description_container.append(description_label)

        percentage_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        percentage_progress = Gtk.ProgressBar()
        percentage_progress.set_fraction(percentage / 100.0)
        percentage_progress.set_show_text(f"{percentage}%")
        percentage_progress.set_hexpand(True) 

        
        percentage_container.append(percentage_progress)

        button_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        add_subtask = Gtk.Button(label="Deletar")
        add_subtask.task = task
        add_subtask.connect("clicked", self.delete_task)
        edit_task = Gtk.Button(label="Editar")
        edit_task.task = task
        edit_task.connect("clicked", self.edit_task)
        button_container.append(add_subtask)
        button_container.append(edit_task)

        button_subtask_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        add_subtask = Gtk.Button(label="Adicionar Subtask")
        add_subtask.connect("clicked", self.create_subtask)
        add_subtask.task = task
        button_subtask_container.append(add_subtask)

        weeks_container = TaskWeeks(SubTaskRepository.list_weeks(task))
        weeks_container.set_vexpand(False) 

        self.append(week_label_container)
        self.append(description_container)
        self.append(button_container)
        self.append(percentage_container)
        self.append(button_subtask_container)
        self.append(weeks_container)

    def delete_task(self, button):
        task = button.task
        TaskRepository.delete_task(task)
        if self.callback:
            self.callback()

    def edit_task(self, button):
        self.clear_content()
        task = button.task
        self.append(TaskCrud(task=task, callback=self.callback))

    def create_subtask(self, button):
        self.clear_content()
        task = button.task
        self.append(SubTaskCrud(task=task, callback=self.callback))

    def clear_content(self):
        while self.get_first_child() is not None:
            child = self.get_first_child()
            self.remove(child)