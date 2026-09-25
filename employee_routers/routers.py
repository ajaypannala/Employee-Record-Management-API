from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeePatch,
    EmployeeResponse
)
from app import crud


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# CREATE
@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    result = crud.create_employee(db, employee)

    if result == "EMAIL_EXISTS":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return result


# GET ALL
@router.get(
    "/",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):

    return crud.get_employees(db)


# GET BY ID
@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = crud.get_employee(
        db,
        employee_id
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# PUT
@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    result = crud.update_employee(
        db,
        employee_id,
        employee
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if result == "EMAIL_EXISTS":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return result


# PATCH
@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def patch_employee(
    employee_id: int,
    employee: EmployeePatch,
    db: Session = Depends(get_db)
):

    result = crud.patch_employee(
        db,
        employee_id,
        employee
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if result == "EMAIL_EXISTS":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return result


# DELETE
@router.delete(
    "/{employee_id}"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):

    employee = crud.delete_employee(
        db,
        employee_id
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }