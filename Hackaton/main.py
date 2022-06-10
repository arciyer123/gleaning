from Project import create_app,mail
from flask_mail import Message


app = create_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

