from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "core"

    def ready(self):
        # Django应用启动时加载插件
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate, sender=self)
        def load_plugins_on_start(sender, **kwargs):
            from .plugin.loader import load_plugins
            load_plugins()
            from .plugin.registry import registry
            print(f'Core app: {len(registry.list_plugins())} plugins registered')
