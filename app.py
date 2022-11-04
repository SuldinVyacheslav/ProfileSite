import sys

from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

# <--------------------> #
#  InitializeBlockStart  #
# <--------------------> #

from config import REVIEW_DATABASE_NAME
from db.model import db, db_init, Review

app = Flask(__name__, template_folder='templates', static_url_path='/static/')

# SQLAlchimy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + REVIEW_DATABASE_NAME

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '34567890oihgfcvbjktrtyuiop'
app.config['SESSION_COOKIE_NAME'] = 'EVM'

db.app = app
db.init_app(app)
# <------------------> #
#  InitializeBlockEnd  #
# <------------------> #

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        try:

            new_review = Review(name=request.form["name"],
                                review=request.form["review"],
                                )

            db.session.add(new_review)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            print(error)
            print("Can't add new review to the Database")
            flash(error, category='error')
            return redirect("/")

        flash("Thanks for your review. It will be added soon.", category='success')
        return redirect("/")
    else:
        reviews = Review.query.all()
        return render_template('index.html', review=reviews)

    # count = 5
    # dict_ = [{'review': f"number -> {x}",
    #           'name' : "ASD" + str(x),
    #           'position': f'number * 2 -> {x * 2}',
    #           'date': f'number ^ 2 -> {x ^ 2}'}
    #          for x in range(count)]


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            with app.app_context():
                db_init()

    app.run(host="0.0.0.0",port=5000)