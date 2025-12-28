from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UiShellSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("theme", models.CharField(default="classic", max_length=50)),
                ("seo_title", models.CharField(blank=True, default="", max_length=200)),
                ("seo_description", models.TextField(blank=True, default="")),
                ("seo_keywords", models.CharField(blank=True, default="", max_length=500)),
                ("og_image", models.CharField(blank=True, default="", max_length=500)),
            ],
            options={
                "db_table": "ui_shell_settings",
            },
        ),
    ]
