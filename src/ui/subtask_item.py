import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.models.repositories.tasks_repository import TaskRepository
from src.models.repositories.subtasks_repository import SubTaskRepository
from src.ui.subtask_crud import SubTaskCrud

class SubtasksItem(Gtk.Box):
    def __init__(self, subtask = None, callback = None, main=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.callback = callback
        self.main = main

        container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        container.get_style_context().add_class("item")
        
        container_item = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        task = TaskRepository.get_task_by_id(subtask.group_task_id)
        check_button = Gtk.CheckButton(label=f" {subtask.description} ")
        check_button.connect("toggled", self.marker_subtask_update, subtask)
        check_button.handler_block_by_func(self.marker_subtask_update)
        check_button.set_active(subtask.status)
        check_button.handler_unblock_by_func(self.marker_subtask_update)
        task_label = Gtk.Label(label=f"{task.name}")
        task_label.get_style_context().add_class("label-task")

        container_action = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        edit_subtask = Gtk.Button(label="Editar")
        edit_subtask.subtask = subtask
        edit_subtask.task = task
        edit_subtask.connect("clicked", self.edit_subtask)
        delete_subtask = Gtk.Button(label="Deletar")
        delete_subtask.subtask = subtask
        delete_subtask.connect("clicked", self.delete_subtask)

        # ---------------------------------- #
        container_item.append(check_button)
        container_item.append(task_label)
        container_action.append(edit_subtask)
        container_action.append(delete_subtask)
        container.append(container_item)
        container.append(container_action)
        self.append(container)


    def marker_subtask_update(self, check_button, subtask):
        new_status = False if subtask.status else True
        subtask.status = new_status
        SubTaskRepository.update_subtask(subtask=subtask)

    def delete_subtask(self, button):
        subtask = button.subtask
        SubTaskRepository.delete_subtask(subtask)
        if self.callback:
            self.callback()

    def edit_subtask(self, button):
        subtask = button.subtask
        task = button.task
        self.main.clear_content()
        self.main.content_box.append(SubTaskCrud(subtask=subtask, task=task, button_label="Atualizar", callback=self.callback))

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