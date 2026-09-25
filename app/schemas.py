from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Used for POST - Create employee
class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    department: str = Field(..., min_length=2)
    salary: float = Field(..., gt=0)
    designation: str = Field(..., min_length=2)


# Used for PUT - Update entire employee
class EmployeeUpdate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    department: str = Field(..., min_length=2)
    salary: float = Field(..., gt=0)
    designation: str = Field(..., min_length=2)


# Used for PATCH - Update selected fields
class EmployeePatch(BaseModel):
    name: str | None = Field(None, min_length=2)
    email: EmailStr | None = None
    department: str | None = Field(None, min_length=2)
    salary: float | None = Field(None, gt=0)
    designation: str | None = Field(None, min_length=2)


# Used for API response
class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    salary: float
    designation: str

    model_config = ConfigDict(from_attributes=True)