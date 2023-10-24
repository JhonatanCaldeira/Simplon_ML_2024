from sqlalchemy import Column, String, Integer, ForeignKey, Double, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    eeid = Column(String(10))
    name = Column(String(255))
    age = Column(Integer)
    hire_date = Column(Date)
    anual_salary = Column(Double)
    bonus = Column(String)
    exit_date = Column(Date)

    job_title_id = Column(Integer, ForeignKey("job_title.id"))
    job_title = relationship("Job_Title")

    department_id = Column(Integer, ForeignKey("department.id"))
    department = relationship("Department")

    business_unit_id = Column(Integer, ForeignKey("business_unit.id"))
    business_unit = relationship("Business_Unit")

    gender_id = Column(Integer, ForeignKey("gender.id"))
    gender = relationship("Gender")

    ethnicity_id = Column(Integer, ForeignKey("ethnicity.id"))
    ethnicity = relationship("Ethnicity")

    city_id = Column(Integer, ForeignKey("city.id"))
    city = relationship("City")

class Job_Title(Base):
    __tablename__ = "Job_Title"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Department(Base):
    __tablename__ = "Department"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Business_Unit(Base):
    __tablename__ = "Business_Unit"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Gender(Base):
    __tablename__ = "Gender"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Ethnicity(Base):
    __tablename__ = "Ethnicity"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Country(Base):
    __tablename__ = "Country"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class City(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    country_id = Column(Integer, ForeignKey("pays.id"))
    pays = relationship("Pays")