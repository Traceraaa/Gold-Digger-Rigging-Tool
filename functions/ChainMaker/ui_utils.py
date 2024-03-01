import maya.cmds as cmds

# UI interaction utility functions


def enable_button():
    pass


def disable_btn():
    pass


def enable_slider(slider):
    """
    enable user slider
    """
    print("Enabling slider")
    if not slider:
        print("Slider is None")
        return

    if cmds.intSliderGrp(slider, q=True, ex=True) or cmds.intSlider(slider, q=True, ex=True):
        cmds.intSliderGrp(slider, e=True, en=True)

    if cmds.floatSliderGrp(slider, q=True, ex=True) or cmds.floatSlider(slider, q=True, ex=True):
        cmds.floatSliderGrp(slider, e=True, en=True)


def disable_slider(slider):
    """
    disable user slider
    """
    print("Disabling slider")
    if not slider:
        print("Slider is None")
        return

    if cmds.intSliderGrp(slider, q=True, ex=True) or cmds.intSlider(slider, q=True, ex=True):
        cmds.intSliderGrp(slider, e=True, en=False)

    if cmds.floatSliderGrp(slider, q=True, ex=True) or cmds.floatSlider(slider, q=True, ex=True):
        cmds.floatSliderGrp(slider, e=True, en=False)



def enable_radio_btn(message):
    print(message)
    # cmds.radioButtonGrp(button, e=True, en=True)

def expand_toggle():
    pass

def collapse_toggle():
    pass




