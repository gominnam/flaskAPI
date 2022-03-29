from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

from flask import Flask
import app.users.views as view

app = Flask(__name__)

app.add_url_rule("/hello", view_func=view.HelloWorld.as_view('hello'))
app.add_url_rule("/myinfo", view_func=view.myInfo.as_view('myinfo'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
