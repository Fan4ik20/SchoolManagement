from pydantic import BaseModel, ValidationError


class StudentSchema(BaseModel):
    first_name: str
    last_name: str
    group_id: int
