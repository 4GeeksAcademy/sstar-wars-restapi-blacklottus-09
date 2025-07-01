from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    favorites = relationship("Favorite", back_populates="user")
    def serialize(self):
        return{
            "id": self.id,
            "email": self.email
        }


class Favorite(db.Model):
    __tablename__ = "favorite"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    favorite_type: Mapped[str] = mapped_column(String(50), nullable=False)
    favorite_id: Mapped[int] = mapped_column(nullable=False)

    user = relationship("User", back_populates="favorites")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id, 
            "favorite_type":self.favorite_type,
            "favorite_id": self.favorite_id
         }


class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=True)
    height: Mapped[int] = mapped_column(nullable=True)
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "birth_year":self.birth_year,
            "height": self.height
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(30), nullable=True)
    population: Mapped[int] = mapped_column(nullable=True)
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "climate":self.climate,
            "population": self.population
        }
