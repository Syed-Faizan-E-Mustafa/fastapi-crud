from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str


class CreateUserResponse(BaseModel):
    name: str


class UpdateUserRequest(BaseModel):
    name: str = None
    email: str = None


class ItemCreateRequest(BaseModel):
    title: str
    description: str
    owner_id: int


class ItemUpdateRequest(BaseModel):
    title: str = None
    description: str = None
    owner_id: int = None
