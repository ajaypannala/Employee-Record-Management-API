from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models
from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeePatch
)


# CREATE
def create_employee(db: Session, employee: EmployeeCreate):

    # Check whether email already exists
    existing_employee = (
        db.query(models.Employee)
        .filter(models.Employee.email == employee.email)
        .first()
    )

    if existing_employee:
        return "EMAIL_EXISTS"

    db_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        salary=employee.salary,
        designation=employee.designation
    )

    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

        return db_employee

    except IntegrityError:
        db.rollback()
        return "EMAIL_EXISTS"


# GET ALL
def get_employees(db: Session):
    return db.query(models.Employee).all()


# GET BY ID
def get_employee(db: Session, employee_id: int):

    return (
        db.query(models.Employee)
        .filter(models.Employee.id == employee_id)
        .first()
    )


# PUT - COMPLETE UPDATE
def update_employee(
    db: Session,
    employee_id: int,
    employee: EmployeeUpdate
):

    # Find employee
    db_employee = get_employee(db, employee_id)

    if db_employee is None:
        return None

    # Check whether email belongs to another employee
    existing_employee = (
        db.query(models.Employee)
        .filter(
            models.Employee.email == employee.email,
            models.Employee.id != employee_id
        )
        .first()
    )

    if existing_employee:
        return "EMAIL_EXISTS"

    db_employee.name = employee.name
    db_employee.email = employee.email
    db_employee.department = employee.department
    db_employee.salary = employee.salary
    db_employee.designation = employee.designation

    try:
        db.commit()
        db.refresh(db_employee)

        return db_employee

    except IntegrityError:
        db.rollback()
        return "EMAIL_EXISTS"


# PATCH - PARTIAL UPDATE
def patch_employee(
    db: Session,
    employee_id: int,
    employee: EmployeePatch
):

    # Find employee
    db_employee = get_employee(db, employee_id)

    if db_employee is None:
        return None

    # Get only fields sent by the user
    update_data = employee.model_dump(
        exclude_unset=True
    )

    # Check email only if email is being updated
    if "email" in update_data:

        existing_employee = (
            db.query(models.Employee)
            .filter(
                models.Employee.email == update_data["email"],
                models.Employee.id != employee_id
            )
            .first()
        )

        if existing_employee:
            return "EMAIL_EXISTS"

    # Update fields
    for field, value in update_data.items():
        setattr(db_employee, field, value)

    try:
        db.commit()
        db.refresh(db_employee)

        return db_employee

    except IntegrityError:
        db.rollback()
        return "EMAIL_EXISTS"


# DELETE
def delete_employee(
    db: Session,
    employee_id: int
):

    db_employee = get_employee(db, employee_id)

    if db_employee is None:
        return None

    try:
        db.delete(db_employee)
        db.commit()

        return db_employee

    except Exception:
        db.rollback()
        raise