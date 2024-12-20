from flask import Flask

app = Flask(__name__)

# Import routes at the end to avoid circular import issues
import app.routes
