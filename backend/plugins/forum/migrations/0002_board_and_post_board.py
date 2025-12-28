from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("forum", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("order", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "forum_boards",
            },
        ),
        migrations.AddField(
            model_name="post",
            name="board",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                related_name="posts",
                to="forum.board",
            ),
        ),
    ]
