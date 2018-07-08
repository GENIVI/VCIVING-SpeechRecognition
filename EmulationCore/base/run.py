import sys, os

relative_emucore_dir = "../EmulationCore"
abs_emucore_dir = os.path.abspath(relative_emucore_dir)
sys.path.append(abs_emucore_dir)

import base.main