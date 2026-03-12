import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

class MessageBox:
    @staticmethod
    def show_info(parent, title: str, message: str, callback=None):
        dialog = Gtk.MessageDialog(
            transient_for=parent,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
            secondary_text=message
        )
        
        dialog.connect("response", lambda d, r: MessageBox._on_response(d, r, callback))
        dialog.present()
        return dialog
    
    @staticmethod
    def show_warning(parent, title: str, message: str, callback=None):
        dialog = Gtk.MessageDialog(
            transient_for=parent,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text=title,
            secondary_text=message
        )
        
        dialog.connect("response", lambda d, r: MessageBox._on_response(d, r, callback))
        dialog.present()
        return dialog
    
    @staticmethod
    def show_error(parent, title: str, message: str, callback=None):
        dialog = Gtk.MessageDialog(
            transient_for=parent,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
            secondary_text=message
        )
        
        dialog.connect("response", lambda d, r: MessageBox._on_response(d, r, callback))
        dialog.present()
        return dialog
    
    @staticmethod
    def show_question(parent, title: str, message: str, callback=None):
        dialog = Gtk.MessageDialog(
            transient_for=parent,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=title,
            secondary_text=message
        )
        
        dialog.connect("response", lambda d, r: MessageBox._on_question_response(d, r, callback))
        dialog.present()
        return dialog
    
    @staticmethod
    def show_confirm(parent, title: str, message: str, callback=None):
        dialog = Gtk.MessageDialog(
            transient_for=parent,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=title,
            secondary_text=message
        )
        
        dialog.connect("response", lambda d, r: MessageBox._on_confirm_response(d, r, callback))
        dialog.present()
        return dialog
    
    @staticmethod
    def show_input(parent, title: str, message: str, default_text: str = "", callback=None):
        dialog = Gtk.MessageDialog(
            transient_for=parent,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=title,
            secondary_text=message
        )
        
        content_area = dialog.get_content_area()
        entry = Gtk.Entry()
        entry.set_text(default_text)
        entry.set_margin_top(10)
        entry.set_margin_bottom(10)
        entry.set_margin_start(20)
        entry.set_margin_end(20)
        content_area.append(entry)
        
        entry.connect("activate", lambda e: dialog.response(Gtk.ResponseType.OK))
        dialog.connect("response", lambda d, r: MessageBox._on_input_response(d, r, entry, callback))        
        GLib.idle_add(entry.grab_focus)
        
        dialog.present()
        return dialog
    
    @staticmethod
    def _on_response(dialog, response, callback):
        dialog.destroy()
        if callback:
            callback()
    
    @staticmethod
    def _on_question_response(dialog, response, callback):
        result = (response == Gtk.ResponseType.YES)
        dialog.destroy()
        if callback:
            callback(result)
    
    @staticmethod
    def _on_confirm_response(dialog, response, callback):
        result = (response == Gtk.ResponseType.OK)
        dialog.destroy()
        if callback:
            callback(result)
    
    @staticmethod
    def _on_input_response(dialog, response, entry, callback):
        text = entry.get_text() if response == Gtk.ResponseType.OK else None
        dialog.destroy()
        if callback:
            callback(text)