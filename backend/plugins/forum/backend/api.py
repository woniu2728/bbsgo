from django.shortcuts import get_object_or_404
from ninja import Router

from plugins.auth.security import AuthBearer
from plugins.forum.backend.models import Board, Comment, Post
from plugins.forum.backend.permissions import can_delete, can_manage_boards, can_post, can_view
from plugins.forum.backend.schemas import (
    BoardCreate,
    BoardOut,
    BoardUpdate,
    CommentCreate,
    CommentOut,
    PostCreate,
    PostOut,
)

router = Router()


@router.get("/posts", response=list[PostOut])
def list_posts(request, board_id: int | None = None):
    if not can_view(getattr(request, "user", None)):
        return 403, {"detail": "forbidden"}
    queryset = Post.objects.all().order_by("-id")
    if board_id is not None:
        queryset = queryset.filter(board_id=board_id)
    return queryset


@router.get("/posts/{post_id}", response=PostOut)
def get_post(request, post_id: int):
    if not can_view(getattr(request, "user", None)):
        return 403, {"detail": "forbidden"}
    return get_object_or_404(Post, id=post_id)


@router.post("/posts", response=PostOut, auth=AuthBearer())
def create_post(request, payload: PostCreate):
    user = request.auth.user
    if not can_post(user):
        return 403, {"detail": "forbidden"}
    post = Post.objects.create(
        author=user,
        title=payload.title,
        content=payload.content,
        board_id=payload.board_id,
    )
    return post


@router.delete("/posts/{post_id}", auth=AuthBearer())
def delete_post(request, post_id: int):
    user = request.auth.user
    post = get_object_or_404(Post, id=post_id)
    if not (can_delete(user) or post.author_id == user.id):
        return 403, {"detail": "forbidden"}
    post.delete()
    return {"ok": True}


@router.get("/comments", response=list[CommentOut])
def list_comments(request, post_id: int):
    if not can_view(getattr(request, "user", None)):
        return 403, {"detail": "forbidden"}
    return Comment.objects.filter(post_id=post_id).order_by("id")


@router.post("/comments", response=CommentOut, auth=AuthBearer())
def create_comment(request, payload: CommentCreate):
    user = request.auth.user
    if not can_post(user):
        return 403, {"detail": "forbidden"}
    post = get_object_or_404(Post, id=payload.post_id)
    comment = Comment.objects.create(post=post, author=user, content=payload.content)
    return comment


@router.delete("/comments/{comment_id}", auth=AuthBearer())
def delete_comment(request, comment_id: int):
    user = request.auth.user
    comment = get_object_or_404(Comment, id=comment_id)
    if not (can_delete(user) or comment.author_id == user.id):
        return 403, {"detail": "forbidden"}
    comment.delete()
    return {"ok": True}


@router.get("/manifest")
def forum_manifest(request):
    return {
        "routes": [{"path": "/forum", "component": "ForumHome"}],
        "menu": {"id": "forum", "label": "Forum", "path": "/forum"},
    }


@router.get("/boards", response=list[BoardOut])
def list_boards(request):
    return Board.objects.filter(is_active=True).order_by("order", "id")


@router.get("/boards/all", response=list[BoardOut], auth=AuthBearer())
def list_all_boards(request):
    if not can_manage_boards(request.auth.user):
        return 403, {"detail": "forbidden"}
    return Board.objects.all().order_by("order", "id")


@router.post("/boards", response=BoardOut, auth=AuthBearer())
def create_board(request, payload: BoardCreate):
    if not can_manage_boards(request.auth.user):
        return 403, {"detail": "forbidden"}
    board = Board.objects.create(
        name=payload.name,
        slug=payload.slug,
        description=payload.description or "",
        order=payload.order or 0,
        is_active=True if payload.is_active is None else payload.is_active,
    )
    return board


@router.put("/boards/{board_id}", response=BoardOut, auth=AuthBearer())
def update_board(request, board_id: int, payload: BoardUpdate):
    if not can_manage_boards(request.auth.user):
        return 403, {"detail": "forbidden"}
    board = get_object_or_404(Board, id=board_id)
    if payload.name is not None:
        board.name = payload.name
    if payload.slug is not None:
        board.slug = payload.slug
    if payload.description is not None:
        board.description = payload.description
    if payload.order is not None:
        board.order = payload.order
    if payload.is_active is not None:
        board.is_active = payload.is_active
    board.save()
    return board


@router.delete("/boards/{board_id}", auth=AuthBearer())
def delete_board(request, board_id: int):
    if not can_manage_boards(request.auth.user):
        return 403, {"detail": "forbidden"}
    board = get_object_or_404(Board, id=board_id)
    board.delete()
    return {"ok": True}
