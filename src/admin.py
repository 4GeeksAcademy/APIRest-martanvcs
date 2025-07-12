import os
from flask_admin import Admin
from models import db, User, Character, Planet, FavoritePlanet, FavoriteCharacter
from flask_admin.contrib.sqla import ModelView
# from flask_admin.form import Select2Widget
# from wtforms_sqlalchemy.fields import QuerySelectField


class UserModelView(ModelView):
    column_list = ['id', 'email', 'first_name',
                   'last_name', 'subscription_date', 'is_active']
    column_searchable_list = ['email', 'first_name', 'last_name']
    column_filters = ['subscription_date', 'is_active']
    form_excluded_columns = ['favorites']


class CharacterModelView(ModelView):
    column_list = ['id', 'name', 'gender', 'birth_year', 'eye_color']
    column_searchable_list = ['name']
    column_filters = ['gender']


class PlanetModelView(ModelView):
    column_list = ['id', 'name', 'climate', 'population', 'terrain']
    column_searchable_list = ['name']
    column_filters = ['climate']


class FavoriteModelView(ModelView):
    column_list = ['id', 'user_id', 'character_id', 'planet_id']
    column_filters = ['user_id', 'character_id', 'planet_id']


class FavoritePlanetModelView(ModelView):
    column_list = ['id', 'user_id', 'planet_id']
    column_filters = ['user_id', 'planet_id']
    form_columns = ['user_id', 'planet_id']


class FavoriteCharacterModelView(ModelView):
    column_list = ['id', 'user_id', 'character_id']
    column_filters = ['user_id', 'character_id']
    form_columns = ['user_id', 'character_id']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(FavoritePlanetModelView(FavoritePlanet, db.session))
    admin.add_view(FavoriteCharacterModelView(FavoriteCharacter, db.session))
