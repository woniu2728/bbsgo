from plugins.ui_shell.api import router


class Plugin:
    def on_enable(self, api):
        api.add_router(router, tags=["ui-shell"])
