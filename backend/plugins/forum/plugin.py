from plugins.forum.backend.api import router
from plugins.forum.backend.hooks import on_user_deleted


class Plugin:
    def on_enable(self, api):
        api.add_router(router, prefix="/forum", tags=["forum"])
        api.subscribe("user_deleted", on_user_deleted)
