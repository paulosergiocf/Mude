import sys
import gi
import os

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gdk
from src.models.repositories.tasks_repository import TaskRepository
class TaskWeeks(Gtk.Box):
    
    def __init__(self, weeks):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.get_style_context().add_class("card-subtasks-day")

        for week in weeks:
            week_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            info_weeks = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            info_percentage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            initial_week_label = Gtk.Label(label="")
            initial_week_label.set_markup(f'<b>{week[0][0]}</b>')
            final_week_label = Gtk.Label(label="")
            final_week_label.set_markup(f'<b>{week[0][1]}</b>')
            percentage_progress = Gtk.ProgressBar()
            percentage_progress.set_fraction(week[1] / 100.0)
            percentage_progress.set_show_text(f"{(week[1] / 100.0)}%")
            percentage_progress.set_hexpand(True)
            percentage_progress.add_css_class("custom-progress")
            info_weeks.append(initial_week_label)
            info_weeks.append(final_week_label)
            info_percentage.append(percentage_progress)

            week_container.append(info_weeks)
            week_container.append(info_percentage)
            self.append(week_container)
 

