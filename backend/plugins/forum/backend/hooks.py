from plugins.forum.backend.models import Comment, Post


def on_user_deleted(user_id: int):
    Comment.objects.filter(author_id=user_id).delete()
    Post.objects.filter(author_id=user_id).delete()
