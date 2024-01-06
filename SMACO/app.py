from flask import Flask
from index import index
from calculator import calculator

app = Flask(__name__)
app.register_blueprint(index,url_prefix="/index")
app.register_blueprint(calculator,url_prefix="/calculator")

if __name__ == '__main__':
    app.run(debug=True)