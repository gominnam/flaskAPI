from flask import Flask
import app.users.views as view

app = Flask(__name__)

app.add_url_rule("/", view_func=view.home.as_view('home'))
app.add_url_rule("/hello", view_func=view.HelloWorld.as_view('hello'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
