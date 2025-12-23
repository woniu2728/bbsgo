from django.apps import AppConfig


class AuthPluginConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plugins.auth"
    label = "auth_plugin"
