from django.db import migrations
from django.contrib.auth.hashers import make_password


def crear_usuarios(apps, schema_editor):
    User = apps.get_model("auth", "User")
    if not User.objects.filter(username="admin").exists():
        User.objects.create(
            username="admin",
            email="admin@example.com",
            password=make_password("holamundo"),
            is_staff=True,
            is_superuser=True,
        )
    if not User.objects.filter(username="cliente").exists():
        User.objects.create(
            username="cliente",
            email="cliente@example.com",
            password=make_password("holamundo123"),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("productos", "0006_orden_itemorden"),
    ]

    operations = [
        migrations.RunPython(crear_usuarios),
    ]
