from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Cuidar App is Running on Vercel!"

# Vercel requires a handler
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
