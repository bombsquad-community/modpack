# ba_plugman

# __name__ : 'mood_setter'

# __author__ : 'brostos'

# __discord__ : 'brostos'

# __description__ : 'Set a custom tint according to your mood'

# __body__ : "This mod changes the background tint of the game. Can be accessed by using the added buttons on the ui"

# __version__ : 1.0.0

# __attachments__ : None

# __important__ : "Works only with BCS modpack"

# ba_meta require api 8

import ast
import babase
import _babase
import bauiv1 as bui
from bauiv1lib.colorpicker import ColorPicker
from bauiv1._hooks import on_button_press_x
from pathlib import Path


class Select_Color:
    def __init__(self):
        self._color = None
        self.path = Path(f"{babase.app.env.python_directory_user}/Tint/last_tint.txt")
        # A hack to let players select any RGB color value through the UI,
        # otherwise this is limited only to pro accounts.
        bui.app.classic.accounts.have_pro = lambda: True

    def _pick_color(self, tag="color"):
        ColorPicker(
            parent=None,
            position=(0, 0),
            delegate=self,
            tag=tag,
        )
        if babase.do_once():
            bui.screenmessage("Click on white to revert changes", color=(0.2, 1, 1))

    def save(self):
        with open(self.path , "w") as f:
            f.write(str(self.color))
       

    def color_picker_selected_color(self, picker, color):
        # The `ColorPicker` calls this method in the delegate once a color
        # is selected from the `ColorPicker` Window.
        if color:
            _babase.set_global_tint(*color)
            self.color = color
            self.save()


    def color_picker_closing(self, picker):
        # The `ColorPicker` expects this method to exist in the delegate,
        # so here it is!
        pass
    
def new_on_button_press_x()->None:
    Select_Color()._pick_color()
     
# ba_meta export plugin
class Mood_selector(babase.Plugin):
    def on_app_running(self):
        try:
            with open(Select_Color().path, "r") as f:
                color = ast.literal_eval(f.read())
                _babase.set_global_tint(*color)
        except FileNotFoundError:
            # Incase of first install
            pass
            
            
        on_button_press_x = new_on_button_press_x