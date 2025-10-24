from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("uauth", "0003_temppassword"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserDeletionStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("pending_since", models.DateTimeField(blank=True, null=True)),
                ("pending_until", models.DateTimeField(blank=True, null=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="deletion_status", to="auth.user")),
            ],
        ),
    ]

