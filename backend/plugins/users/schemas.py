from ninja import Schema


class UserOut(Schema):
    id: int
    username: str
    email: str | None
    display_name: str | None
    is_active: bool

    class Config:
        from_attributes = True


class UserCreate(Schema):
    username: str
    password: str
    email: str | None = None
    display_name: str | None = None


class UserUpdate(Schema):
    email: str | None = None
    display_name: str | None = None
    is_active: bool | None = None
