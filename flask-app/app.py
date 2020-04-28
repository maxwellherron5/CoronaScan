from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mentions.db'
db = SQLAlchemy(app)

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subreddit = db.Column(db.String(200), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
