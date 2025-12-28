from ninja import Schema


class PostOut(Schema):
    id: int
    board_id: int | None
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True


class PostCreate(Schema):
    board_id: int | None = None
    title: str
    content: str


class CommentOut(Schema):
    id: int
    post_id: int
    author_id: int
    content: str

    class Config:
        from_attributes = True


class CommentCreate(Schema):
    post_id: int
    content: str


class BoardOut(Schema):
    id: int
    name: str
    slug: str
    description: str | None
    order: int
    is_active: bool

    class Config:
        from_attributes = True


class BoardCreate(Schema):
    name: str
    slug: str
    description: str | None = None
    order: int | None = 0
    is_active: bool | None = True


class BoardUpdate(Schema):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    order: int | None = None
    is_active: bool | None = None
