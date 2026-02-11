# Run this to run the Flask application, by importing the function from __init__.py
from app import createApp

app = createApp()

if __name__ == '__main__':
    app.run(debug=True)