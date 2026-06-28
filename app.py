from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import InputRequired
from datetime import datetime, timezone
from os import environ
from time import sleep

from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    celsius = db.Column(db.Float, nullable=False)
    fahrenheit = db.Column(db.Float, nullable=False)
    date = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(200), nullable=False)

class TemperatureForm(FlaskForm):
    celsius = FloatField('Celsius', validators=[InputRequired()])
    submit = SubmitField('Convert')

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit, rounded to two decimal places."""
    return round((float(celsius) * 1.8) + 32, 2)


def _database_uri():
    db_user = environ.get('DB_USER', 'tempconverter')
    db_pass = environ.get('DB_PASS', 'change-me')
    db_host = environ.get('DB_HOST', 'db')
    db_name = environ.get('DB_NAME', 'tempconverter')
    return URL.create(
        'mysql+pymysql',
        username=db_user,
        password=db_pass,
        host=db_host,
        database=db_name,
    )


def _initialize_database(app):
    attempts = int(environ.get('DB_CONNECT_ATTEMPTS', '30'))
    with app.app_context():
        for attempt in range(1, attempts + 1):
            try:
                db.create_all()
                return
            except SQLAlchemyError:
                if attempt == attempts:
                    raise
                app.logger.warning('Database unavailable (attempt %s/%s)', attempt, attempts)
                sleep(2)


def create_app(config=None, initialize_database=True):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=environ.get('SECRET_KEY', 'development-only-change-me'),
        SQLALCHEMY_DATABASE_URI=_database_uri(),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config:
        app.config.update(config)

    db.init_app(app)
    student = environ.get('STUDENT', 'Default Student')
    college = environ.get('COLLEGE', 'Default College')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = TemperatureForm()
        if form.validate_on_submit():
            celsius = float(form.celsius.data)
            temperature = Temperature(
                celsius=celsius,
                fahrenheit=celsius_to_fahrenheit(celsius),
                ip_address=request.remote_addr or 'unknown',
                user_agent=request.user_agent.string or 'unknown',
            )
            db.session.add(temperature)
            db.session.commit()
        temperatures = Temperature.query.order_by(Temperature.date.desc()).limit(10).all()
        log_entries = [
            (
                item.date.strftime('%m/%d/%Y %I:%M:%S %p'),
                item.celsius,
                item.fahrenheit,
                item.ip_address,
                item.user_agent.split()[0],
            )
            for item in temperatures
        ]
        return render_template(
            'index.html', form=form, log_entries=log_entries,
            student=student, college=college,
        )

    @app.get('/healthz')
    def healthz():
        try:
            db.session.execute(text('SELECT 1'))
            return {'status': 'ok'}, 200
        except SQLAlchemyError:
            return {'status': 'database unavailable'}, 503

    if initialize_database:
        _initialize_database(app)
    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=False)
