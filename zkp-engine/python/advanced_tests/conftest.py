import sys
import os

# Insert the parent directory (the "python" folder) so that the "src" package is found.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
