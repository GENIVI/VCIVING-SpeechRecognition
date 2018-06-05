import sys, os

relative_brain_dir = "../Brain"
abs_brain_dir = os.path.abspath(relative_brain_dir)
sys.path.append(abs_brain_dir)

relative_emucore_dir = "../EmulationCore"
abs_emucore_dir = os.path.abspath(relative_emucore_dir)
sys.path.append(abs_emucore_dir)

import base.main