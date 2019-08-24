import sys
#for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, PickleType

#for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

#for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

#for configuration
from sqlalchemy import create_engine

#create declarative_base instance
Base = declarative_base()

#we'll add classes here

#we create the class Book and extend it from the Base Class.
class Recipe(Base):
  __tablename__ = 'recipe'

  id = Column(Integer, primary_key=True)
  title = Column(String(250), nullable=False)
  filenames = Column(PickleType(), nullable=False)
  image = Column(PickleType(), nullable=False)
  ingredients = Column(PickleType(), nullable=False)
  steps = Column(PickleType(), nullable=False)

  @property
  def serialize(self):
     return {
        'title': self.title,
        'filenames': self.filenames,
        'image': self.image,
        'ingredients': self.ingredients,
        'steps': self.steps,
     }

#creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///recipes.db')

Base.metadata.create_all(engine)