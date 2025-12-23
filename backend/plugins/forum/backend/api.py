from django.shortcuts import get_object_or_404
from ninja import Router

from plugins.auth.security import AuthBearer
from plugins.forum.backend.models import Comment, Post
from plugins.forum.backend.permissions import can_delete, can_post, can_view
from plugins.forum.backend.schemas import CommentCreate, CommentOut, PostCreate, PostOut

router = Router()


@router.get("/posts", response=list[PostOut])
def list_posts(request):
    if not can_view(getattr(request, "user", None)):
        return 403, {"detail": "forbidden"}
    return Post.objects.all().order_by("-id")


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
    post = Post.objects.create(author=user, title=payload.title, content=payload.content)
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
