from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PluginRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("version", models.CharField(max_length=50)),
                ("enabled", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "core_plugin_records",
            },
        ),
        migrations.CreateModel(
            name="Permission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=100, unique=True, verbose_name="权限代码")),
                ("name", models.CharField(blank=True, max_length=200, verbose_name="权限名称")),
                ("description", models.TextField(blank=True, verbose_name="权限描述")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
            ],
            options={
                "db_table": "rbac_permissions",
                "verbose_name": "权限",
                "verbose_name_plural": "权限",
            },
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="角色名称")),
                ("description", models.TextField(blank=True, verbose_name="角色描述")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
            ],
            options={
                "db_table": "rbac_roles",
                "verbose_name": "角色",
                "verbose_name_plural": "角色",
            },
        ),
        migrations.CreateModel(
            name="RolePermission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("permission", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="roles", to="core.permission", verbose_name="权限")),
                ("role", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="permissions", to="core.role", verbose_name="角色")),
            ],
            options={
                "db_table": "rbac_role_permissions",
                "verbose_name": "角色权限",
                "verbose_name_plural": "角色权限",
                "unique_together": {("role", "permission")},
            },
        ),
        migrations.CreateModel(
            name="UserRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("role", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="users", to="core.role")),
                ("user", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="rbac_roles", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "rbac_user_roles",
                "verbose_name": "用户角色",
                "verbose_name_plural": "用户角色",
                "unique_together": {("user", "role")},
            },
        ),
    ]
