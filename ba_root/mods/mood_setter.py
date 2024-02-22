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

import bauiv1 as bui
import babase
import _babase
import ui_hooks
from bauiv1lib.colorpicker import ColorPicker
from bauiv1lib import mainmenu

original_have_pro = None

class MoodSetterWindow(bui.Window):
    def __init__(self, default_color=((1, 1, 1))):
        self._default_color = default_color
        self._color = babase.app.config.get("MoodSetter", (None))

        self._last_color = self._color
        self.color = self._color or self._default_color


        # A hack to let players select any RGB color value through the UI,
        # otherwise this is limited only to pro accounts.
        bui.app.classic.accounts.have_pro = lambda: True

    def draw_ui(self):
        # NOTE: Most of the stuff here for drawing the UI is referred from the
        # legacy (1.6 < version <= 1.7.19) game's bastd/ui/profile/edit.py, and
        # so there could be some cruft here due to my oversight.
        uiscale = bui.app.ui_v1.uiscale
        self._width = width = 480.0 if uiscale is babase.UIScale.SMALL else 380.0
        self._x_inset = x_inset = 40.0 if uiscale is babase.UIScale.SMALL else 0.0
        self._height = height = (
            275.0
            if uiscale is babase.UIScale.SMALL
            else 288.0
            if uiscale is babase.UIScale.MEDIUM
            else 300.0
        )
        spacing = 40
        self._base_scale = (
            2.05
            if uiscale is babase.UIScale.SMALL
            else 1.5
            if uiscale is babase.UIScale.MEDIUM
            else 1.0
        )
        top_extra = 15

        super().__init__(
            root_widget=bui.containerwidget(
                size=(width, height + top_extra),
                on_outside_click_call=babase.Call(self.cancel_on_outside_click),
                transition="in_right",
                scale=self._base_scale,
                stack_offset=(0, 15) if uiscale is babase.UIScale.SMALL else (0, 0),
            )
        )

        cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(52 + x_inset, height - 60),
            size=(155, 60),
            scale=0.8,
            autoselect=True,
            label=babase.Lstr(resource="cancelText"),
            on_activate_call=self._cancel,
        )
        bui.containerwidget(edit=self._root_widget, cancel_button=cancel_button)

        save_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(width - (177 + x_inset), height - 110),
            size=(155, 60),
            autoselect=True,
            scale=0.8,
            label=babase.Lstr(resource="saveText"),
        )
        bui.widget(edit=save_button, left_widget=cancel_button)
        bui.buttonwidget(edit=save_button, on_activate_call=self.save)
        bui.widget(edit=cancel_button, right_widget=save_button)
        bui.containerwidget(edit=self._root_widget, start_button=save_button)

        reset_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(width - (177 + x_inset), height - 60),
            size=(155, 60),
            color=(0.2, 0.5, 0.6),
            autoselect=True,
            scale=0.8,
            label=babase.Lstr(resource="settingsWindowAdvanced.resetText"),
        )
        bui.widget(edit=reset_button, left_widget=reset_button)
        bui.buttonwidget(edit=reset_button, on_activate_call=self.reset)
        bui.widget(edit=cancel_button, right_widget=reset_button)
        bui.containerwidget(edit=self._root_widget, start_button=reset_button)

        v = height - 65.0
        v -= spacing * 3.0
        b_size = 80
        b_offs = 75

        self._color_button = bui.buttonwidget(
            parent=self._root_widget,
            autoselect=True,
            position=(self._width * 0.5 - b_offs - b_size * 0.5, v - 50),
            size=(b_size, b_size),
            color=self._last_color or self._default_color,
            label="",
            button_type="square",
        )
        bui.buttonwidget(
            edit=self._color_button,
            on_activate_call=babase.Call(self._pick_color, "color"),
        )
        bui.textwidget(
            parent=self._root_widget,
            h_align="center",
            v_align="center",
            position=(self._width * 0.5 - b_offs, v - 65),
            size=(0, 0),
            draw_controller=self._color_button,
            text=babase.Lstr(resource="editProfileWindow.colorText"),
            scale=0.7,
            color=bui.app.ui_v1.title_color,
            maxwidth=120,
        )

    def _pick_color(self, tag):
        if tag == "color":
            initial_color = self.color
        ColorPicker(
            parent=None,
            position=(0, 0),
            initial_color=initial_color,
            delegate=self,
            tag=tag,
        )


    def cancel_on_outside_click(self):
        # I wonder why
        pass
        # bui.getsound("swish").play()
        # babase.Call(self._cancel)

    def _cancel(self):
        if self._last_color:
            _babase.set_global_tint(*self._last_color)
        # Good idea to revert this back now so we do not break anything else.
        # bui.app.classic.accounts.have_pro = original_have_pro
        bui.containerwidget(edit=self._root_widget, transition="out_right")
    

    def reset(self, transition_out=True):
        if transition_out:
            bui.getsound("gunCocking").play()
        babase.app.config["MoodSetter"] = (1, 1, 1)
        babase.app.config.commit()
        _babase.disable_custom_tint()
        # Good idea to revert this back now so we do not break anything else.
        # bui.app.classic.accounts.have_pro = original_have_pro
        bui.containerwidget(edit=self._root_widget, transition="out_right")
            

    def save(self, transition_out=True):
        if transition_out:
            bui.getsound("gunCocking").play()
        _babase.set_global_tint(*self._color)
        self._last_color = self._color
        babase.app.config["MoodSetter"] = self._color
        babase.app.config.commit()
        # Good idea to revert this back now so we do not break anything else.
        # bui.app.classic.accounts.have_pro = original_have_pro
        bui.containerwidget(edit=self._root_widget, transition="out_right")
    
    def _set_color(self, color):
        self._color = color
        _babase.set_global_tint(*self._color)

        if self._color_button:
            bui.buttonwidget(edit=self._color_button, color=color)

    def color_picker_selected_color(self, picker, color):
        # The `ColorPicker` calls this method in the delegate once a color
        # is selected from the `ColorPicker` Window.
        if not self._root_widget:
            return
        tag = picker.get_tag()
        if tag == "color":
            self._set_color(color=color)

    def color_picker_closing(self, picker):
        # The `ColorPicker` expects this method to exist in the delegate,
        # so here it is!
        pass
    
class NewMainMenuWindow(mainmenu.MainMenuWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Display chat icon, but if user open/close gather it may disappear
        bui.set_party_icon_always_visible(True)

def new_on_button_x_press(arg):
    if arg == "X":
        MoodSetterWindow().draw_ui()
    if arg == "Y":
        print("button Y pressed from UI or keyboard")
    
    
# ba_meta export plugin
class Mood_selector(babase.Plugin):
    def on_app_running(self) -> None:
        _babase.set_global_tint(*MoodSetterWindow().color)
        mainmenu.MainMenuWindow = NewMainMenuWindow
        ui_hooks.on_button_xy_press = new_on_button_x_press
        
        
    def has_settings_ui(self):
        return True

    def show_settings_ui(self, source_widget):
        MoodSetterWindow().draw_ui()
