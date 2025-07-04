import os
from flask_admin import Admin
from models import db, User, Character, Planet, Favorite
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    column_list = ['id', 'email', 'first_name',
                   'last_name', 'subscription_date', 'is_active']


class CharacterModelView(ModelView):
    column_list = ['id', 'name', 'gender', 'birth_year', 'eye_color']


class PlanetModelView(ModelView):
    column_list = ['id', 'name', 'climate', 'population', 'terrain']


class FavoriteModelView(ModelView):
    column_list = ['id', 'user_id', 'character_id', 'planet_id']


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
    admin.add_view(FavoriteModelView(Favorite, db.session))
