from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from emailDelivery import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:inner123@localhost/salary_collector'

app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://qoyodgkuqvbkkn:c86a344460ea76865b4699cc8d7ba576fe22e36597e8c6dd8a55d6b7ff1cfff0@ec2-34-225-82-212.compute-1.amazonaws.com:5432/dapi4ovi3kvvq6?sslmode=require'


db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "salary_data_table"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    salary_ = db.Column(db.Integer)

    def __init__(self, email_, salary_):
        self.email_ = email_
        self.salary_ = salary_


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_address_name"]
        salary = request.form["salary_name"]
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, salary)
            db.session.add(data)
            db.session.commit()
            average_salary = db.session.query(func.avg(Data.salary_)).scalar()
            average_salary = round(average_salary, 0)
            count = db.session.query(Data.salary_).count()
            send_email(email, salary, count, average_salary)
            return render_template("success.html")
    return render_template('index.html',
    text="Opps! This email address already exist in our record.")

if __name__ == '__main__':
    app.debug = True
    app.run()