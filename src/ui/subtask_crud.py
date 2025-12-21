import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.models.repositories.tasks_repository import TaskRepository
from src.models.repositories.subtasks_repository import SubTaskRepository
from datetime import date
from src.util.date_util import DateUtil

class SubTaskCrud(Gtk.Box):
    def __init__(self, subtask=None, task=None, button_label= "Criar", callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.get_style_context().add_class("card-task")
        self.callback = callback

        description_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        description_entry_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        description_label = Gtk.Label(label="Descrição")
        self.entry_description = Gtk.Entry()
        self.entry_description.set_hexpand(True) 
        description_container.append(description_label)
        description_entry_container.append(self.entry_description)

        date_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        date_entry_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        date_label = Gtk.Label(label="Data")
        self.entry_date = Gtk.Calendar()
        self.entry_date.add_css_class('custom-calendar') 
        self.entry_date.set_hexpand(True) 
        date_container.append(date_label)
        date_entry_container.append(self.entry_date)

        confirm_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        crud_task = Gtk.Button(label=button_label)
        crud_task.set_hexpand(True) 
        
        if subtask:
            crud_task.connect("clicked", self.edit_subtask)
            crud_task.task = task
            crud_task.subtask = subtask
            self.entry_description.set_text(subtask.description)
            
        else:
            crud_task.connect("clicked", self.create_subtask)
            crud_task.task = task

        confirm_container.append(crud_task)

        self.append(description_container)
        self.append(description_entry_container)
        if not subtask:
            self.append(date_container)
            self.append(date_entry_container)
        self.append(confirm_container)

   
    def edit_subtask(self, button):

        subtask = button.subtask

        try:
            description = self.entry_description.get_text()  
            subtask.task = button.task                  
            SubTaskRepository.update_all_subtask(subtask=subtask, description=description)
        
        except Exception as erro:
            raise erro
        if self.callback:
            self.callback()

    def create_subtask(self, button):
        
        try:
            description = self.entry_description.get_text()
            gdt: GLib.DateTime = self.entry_date.get_date()
            year = int(gdt.get_year())
            month = int(gdt.get_month())
            day = int(gdt.get_day_of_month())
            due_date = f"{year}-{month}-{day}"
            task = button.task
            
            SubTaskRepository.create_subtask(description=description,due_date=due_date,task=task)
        
        except Exception as erro:
            raise erro

        if self.callback:
            self.callback()