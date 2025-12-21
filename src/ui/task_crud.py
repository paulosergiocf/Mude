import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.models.repositories.tasks_repository import TaskRepository
from datetime import date
from src.util.date_util import DateUtil

class TaskCrud(Gtk.Box):
    def __init__(self, task=None, button_label= "Criar", callback=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.get_style_context().add_class("card-task")
        self.callback = callback

        name_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        name_entry_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        name_label = Gtk.Label(label="nome")
        self.entry_name = Gtk.Entry()
        self.entry_name.set_hexpand(True) 
        name_container.append(name_label)
        name_entry_container.append(self.entry_name)

        description_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        description_entry_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        description_label = Gtk.Label(label="Descrição")
        self.entry_description = Gtk.Entry()
        self.entry_description.set_hexpand(True) 
        description_container.append(description_label)
        description_entry_container.append(self.entry_description)

        date_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        date_entry_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        date_label = Gtk.Label(label="Data de Início")
        self.entry_date = Gtk.Calendar()
        self.entry_date.add_css_class('custom-calendar') 
        self.entry_date.set_hexpand(True) 
        date_container.append(date_label)
        date_entry_container.append(self.entry_date)

        confirm_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        crud_task = Gtk.Button(label=button_label)
        crud_task.set_hexpand(True) 
        
        if task:
            crud_task.connect("clicked", self.edit_task)
            crud_task.task = task
            self.entry_name.set_text(task.name)
            self.entry_description.set_text(task.description)
            
        else:
            crud_task.connect("clicked", self.create_subtask)

        confirm_container.append(crud_task)

        self.append(name_container)
        self.append(name_entry_container)
        self.append(description_container)
        self.append(description_entry_container)
        self.append(date_container)
        self.append(date_entry_container)
        self.append(confirm_container)

   
    def edit_task(self, button):
        task = button.task
        try:
            task.name = self.entry_name.get_text()
            task.description = self.entry_description.get_text()
            gdt: GLib.DateTime = self.entry_date.get_date()
            year = int(gdt.get_year())
            month = int(gdt.get_month())
            day = int(gdt.get_day_of_month())
            task.start_date = date(year, month, day)
            task.end_date = DateUtil.get_final_date(task.start_date)

            TaskRepository.update_task(task=task)
        
        except Exception as erro:
            raise erro

        if self.callback:
            self.callback()

    def create_subtask(self, button):
        
        try:
            name = self.entry_name.get_text()
            description = self.entry_description.get_text()
            gdt: GLib.DateTime = self.entry_date.get_date()
            year = int(gdt.get_year())
            month = int(gdt.get_month())
            day = int(gdt.get_day_of_month())
            start_date = date(year, month, day)
            end_date = DateUtil.get_final_date(start_date)

            TaskRepository.create_task(name=name, description=description,
                start_date=start_date, end_date=end_date
            )
        
        except Exception as erro:
            raise erro

        if self.callback:
            self.callback()