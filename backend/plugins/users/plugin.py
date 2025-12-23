from plugins.users.api import router


class Plugin:
    def on_enable(self, api):
        api.add_router(router, tags=["users"])
