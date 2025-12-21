from django.db import models


class Permission(models.Model):
    """权限模型"""
    code = models.CharField(max_length=100, unique=True, verbose_name="权限代码")
    name = models.CharField(max_length=200, blank=True, verbose_name="权限名称")
    description = models.TextField(blank=True, verbose_name="权限描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "rbac_permissions"
        verbose_name = "权限"
        verbose_name_plural = "权限"

    def __str__(self):
        return f"{self.code}"


class Role(models.Model):
    """角色模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name="角色名称")
    description = models.TextField(blank=True, verbose_name="角色描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "rbac_roles"
        verbose_name = "角色"
        verbose_name_plural = "角色"

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    """角色权限关联模型"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions", verbose_name="角色")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="roles", verbose_name="权限")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "rbac_role_permissions"
        unique_together = ("role", "permission")
        verbose_name = "角色权限"
        verbose_name_plural = "角色权限"

    def __str__(self):
        return f"{self.role.name} - {self.permission.code}"