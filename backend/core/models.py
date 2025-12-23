from django.db import models


class PluginRecord(models.Model):
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "core_plugin_records"

    def __str__(self) -> str:
        return f"{self.name}:{self.version}"


from core.rbac.models import Permission, Role, RolePermission, UserRole  # noqa: E402,F401
