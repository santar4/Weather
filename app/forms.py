from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class CityForm(FlaskForm):
    city = StringField('Введіть місто', validators=[DataRequired()])
    submit = SubmitField('Отримати прогноз')


class SignupForm(FlaskForm):
    nickname = StringField('Нікнейм', validators=[DataRequired()])
    email = StringField('Електронна пошта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), validators.Length(min=4),])
    confirm_password = PasswordField('Підтвердити пароль', validators=[DataRequired(), EqualTo('password',
                                                                                               message='Паролі повинні співпадати')])
    submit = SubmitField('Зареєструватися')


class LoginForm(FlaskForm):
    nickname = StringField("Ім'я", validators=[validators.DataRequired()])
    password = PasswordField("Пароль", validators=[
        validators.DataRequired(),
        validators.Length(min=4),
    ])
    submit = SubmitField("Увійти")
