import os, inspect, sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)

os.chdir(parent_dir)
sys.path.insert(0, parent_dir)

import cdcwonderpy