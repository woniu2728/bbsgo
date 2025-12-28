from ninja import Schema


class PostOut(Schema):
    id: int
    title: str
    content: str
    author_id: int

    class Config:
        from_attributes = True


class PostCreate(Schema):
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
