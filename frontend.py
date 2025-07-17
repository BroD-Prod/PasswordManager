from flask import Flask, render_template
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = os.getenv("KEY")

@app.route('/index')
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run('0.0.0.0', 5001)