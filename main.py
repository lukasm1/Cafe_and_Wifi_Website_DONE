from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
bootstrap = Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


choices = ["Yes", "No"]


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = URLField('Map URL', validators=[DataRequired(), URL()])
    img_url = URLField('Img URL', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    has_toilet = SelectField('Has toilet?', choices=choices, validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi?', choices=choices, validators=[DataRequired()])
    has_sockets = SelectField('Has Sockets?', choices=choices, validators=[DataRequired()])
    can_take_calls = SelectField('Can take calls?', choices=choices, validators=[DataRequired()])
    coffee_price = StringField('Coffee price', validators=[DataRequired()])

    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/delete.html")
def update():
    cafes = db.session.query(Cafe).all()
    cafes_names_list = []
    for cafe in cafes:
        cafes_names_list.append(cafe.name)
    return render_template("delete.html", cafes=cafes, cafes_names=sorted(cafes_names_list))


@app.route("/find.html")
def find():
    cafes = db.session.query(Cafe).all()
    return render_template("find.html", cafes=cafes)


@app.route('/add.html', methods=["GET", "POST"])
def add():
    form = CafeForm()

    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data.title(),  # 2nd way to tap into form data
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location").title(),
            has_sockets=bool(request.form.get("has_sockets")),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('find'))
    # return jsonify(response={"success": "Successfully added the new cafe."}), 200

    return render_template('add.html', form=form)


@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
    return redirect(url_for('update'))


if __name__ == '__main__':
    app.run(debug=True)