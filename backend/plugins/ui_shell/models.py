from django.db import models


class UiShellSettings(models.Model):
    theme = models.CharField(max_length=50, default="classic")
    seo_title = models.CharField(max_length=200, blank=True, default="")
    seo_description = models.TextField(blank=True, default="")
    seo_keywords = models.CharField(max_length=500, blank=True, default="")
    og_image = models.CharField(max_length=500, blank=True, default="")

    class Meta:
        db_table = "ui_shell_settings"

    def __str__(self) -> str:
        return f"UiShellSettings({self.id})"
