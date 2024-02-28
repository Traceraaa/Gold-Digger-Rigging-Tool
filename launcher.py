import sys

sys.path.insert(0, 'E:\\MayaTools\\Gold-Digger-Rigging-Tool')

from importlib import reload


import ui_spawner_template


reload(ui_spawner_template)
ui_spawner_template.open_window()