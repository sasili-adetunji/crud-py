import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

@app.route('/')
def index():
  return "hello world"


if __name__ == "__main__":
    app.run(port=5000)

