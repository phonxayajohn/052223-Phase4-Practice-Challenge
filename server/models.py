from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    # add relationship
    appearances = db.relationship("Appearance", cascade="all, delete", backref="episode")

    # add serialization rules
    serialize_rules = ("-appearances.episode",)
    

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    # add relationship
    appearances = db.relationship("Appearance", cascade="all, delete", backref="guest")
    
    # add serialization rules
    serialize_rules = ("-appearances.guest",)
    

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    # add relationships
    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"))
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"))
    
    # add serialization rules
    serialize_rules = ("-episode.appearances", "-guest.appearances")
    
    # add validation
    @validates('rating')
    def validates_rating(self, key, rating):
        if not 1 <= rating <= 5:
            raise ValueError("Invalid rating. Please selecting rating 1-5")
        return rating
    
# add any models you may need.
