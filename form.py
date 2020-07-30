from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import data_required

class Coordenadas(FlaskForm):
    archivo = FileField()