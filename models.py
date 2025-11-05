# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    equipment = relationship("Equipment", back_populates="category")

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="equipment")
    reservations = relationship("Reservation", back_populates="equipment")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    equipment_id = Column(Integer, ForeignKey("equipment.id"))

    equipment = relationship("Equipment", back_populates="reservations")