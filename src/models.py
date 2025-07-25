from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    subscription_date: Mapped[date] = mapped_column(default=date.today)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planets: Mapped[list["FavoritePlanet"]] = relationship(
        "FavoritePlanet", back_populates="user"
    )
    favorite_characters: Mapped[list["FavoriteCharacter"]] = relationship(
        "FavoriteCharacter", back_populates="user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat()
        }


class Character(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(20))

    favorites: Mapped[list["FavoriteCharacter"]] = relationship(
        "FavoriteCharacter", back_populates="character"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    population: Mapped[int] = mapped_column(Integer)
    terrain: Mapped[str] = mapped_column(String(100))

    favorites: Mapped[list["FavoritePlanet"]] = relationship(
        "FavoritePlanet", back_populates="planet"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorite_characters")
    character: Mapped["Character"] = relationship("Character", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
