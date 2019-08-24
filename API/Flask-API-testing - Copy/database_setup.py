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
  title = Column(String(250), nullable=True)

#   @property
#   def serialize(self):
#      return {
#         'title': self.title,
#         'filenames': self.filenames,
#         'image': self.image,
#         'ingredients': self.ingredients,
#         'steps': self.steps,
#      }

class Ingredient(Base):
   __tablename__ = "ingredients"

   id = Column(Integer, primary_key=True)
   ingredient = Column(String, nullable=False)
   recipe_id = Column(Integer, ForeignKey("recipe.id"))

   recipe = relationship("Recipe", back_populates="ingredients")

Recipe.ingredients = relationship("Ingredient", order_by=Ingredient.id, back_populates="recipe")

class Step(Base):
   __tablename__ = "steps"

   id = Column(Integer, primary_key=True)
   step = Column(String, nullable=False)
   recipe_id = Column(Integer, ForeignKey("recipe.id"))

   recipe = relationship("Recipe", back_populates="steps")

Recipe.steps = relationship("Step", order_by=Step.id, back_populates="recipe")

class Image(Base):
   __tablename__ = "images"

   id = Column(Integer, primary_key=True)
   filename = Column(String, nullable=False)
   image = Column(String, nullable=False)
   recipe_id = Column(Integer, ForeignKey("recipe.id"))

   recipe = relationship("Recipe", back_populates="images")

Recipe.images = relationship("Image", order_by=Image.id, back_populates="recipe")

#creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///recipes.db')

Base.metadata.create_all(engine)