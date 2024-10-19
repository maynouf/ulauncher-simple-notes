import os
import subprocess
from datetime import datetime

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import (
    KeywordQueryEvent,
    ItemEnterEvent,
    PreferencesEvent,
    PreferencesUpdateEvent,
)
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
# from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.OpenAction import OpenAction


class NoteExtension(Extension):
    """The base extension"""

    def __init__(self):
        super(NoteExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateListener())
        self.subscribe(PreferencesEvent, PreferencesEventListener())

    def notify_user(self, title, message):
        """ Function to show a notification to the user using notify-send """
        try:
            subprocess.run(['notify-send', title, message], check=True)
        except FileNotFoundError:
            print("Error: notify-send command not found. Please install it.")


    def check_write_access_to_note(self, file_path):
        """ Function to check if the user has write access to the note file """
        file_path = os.path.expanduser(file_path)
        try:
            with open(file_path, 'a'):
                pass
            return True
        except IOError:
            self.notify_user("Error", f"No write access to {file_path}. Please check the file path.")
        return False


class KeywordQueryEventListener(EventListener):
    """Listens to keyboard events"""

    def on_event(self, event: KeywordQueryEvent, extension: Extension):
        file_path = os.path.expanduser(extension.preferences["note_path"])
        note_kw = extension.preferences["note_kw"]
        open_arg = extension.preferences["open_arg"]
        keyword = event.get_keyword()
        note_text = event.get_argument()

        if note_text:
            if keyword == note_kw and note_text == open_arg:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/icon.png',
                        name="Open notes",
                        description=f"Open notes in {file_path}",
                        on_enter=OpenAction(file_path)
                    )
                ])

            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=f"Write '{note_text}' to {file_path}.",
                    description=f"Append text to {file_path}.",
                    on_enter=ExtensionCustomAction(note_text, keep_app_open=False)
                )
            ])
        return RenderResultListAction([])


class ItemEnterEventListener(EventListener):
    """Listens to enters"""
    def on_event(self, event: ItemEnterEvent, extension: Extension):
        text_to_write = event.get_data()
        file_path = extension.preferences["note_path"]
        file_path = os.path.expanduser(file_path)

        include_date = extension.preferences["date_timestamp"] == "true"
        include_time = extension.preferences["time_timestamp"] == "true"

        if include_date and include_time:
            text_to_write = "[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "] " + text_to_write
        elif include_date:
            text_to_write = "[" + str(datetime.now().date()) + "] " + text_to_write
        elif include_time:
            text_to_write = "[" + str(datetime.now().strftime("%H:%M:%S")) + "] " + text_to_write
        append_to_note(file_path, text_to_write)


class PreferencesUpdateListener(EventListener):
    """Executed when preferences are changed"""
    def on_event(self, event: PreferencesUpdateEvent, extension: Extension):
        if event.id == "note_path":
            file_path = event.new_value
            if not extension.check_write_access_to_note(file_path):
                return None
        extension.preferences[event.id] = event.new_value


class PreferencesEventListener(EventListener):
    """Executed on startup"""
    def on_event(self, event: PreferencesEvent, extension: Extension):
        file_path = event.preferences.get("note_path")
        if not extension.check_write_access_to_note(file_path):
            return None

        extension.preferences.update(event.preferences)


def append_to_note(file_path, text):
    """ Function to append text to a note file """
    with open(file_path, 'a') as note_file:
        note_file.write(text + '\n' + '\n')


if __name__ == '__main__':
    """The main function"""
    NoteExtension().run()
