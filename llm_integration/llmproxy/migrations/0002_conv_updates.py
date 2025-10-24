from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("llmproxy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="conversation",
            name="uploaded_pdf_url",
            field=models.URLField(blank=True, default=""),
        ),
    ]

