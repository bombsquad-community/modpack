# This files aim is to add mutation support for the newly added buttons(x and y)
# Do the patching by importing ui_hooks but not from ui_hooks import on_button_xy_press it wont work
# ui_hooks.on_button_xy_press = some_function 
# is the correct way.

def on_button_xy_press(arg) -> None:
    if arg == "X":
        print("button X pressed from UI or keyboard")
    if arg == "Y":
        print("button Y pressed from UI or keyboard")