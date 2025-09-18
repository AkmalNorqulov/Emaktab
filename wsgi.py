import sys
import os
from app import app  # replace with your Flask app instance

# Add your project path so Python can find it
sys.path.insert(0, os.path.dirname(__file__))

application = app  # WSGI expects "application"