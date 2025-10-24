from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("llmproxy", "0002_conv_updates"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="pdf_context_md",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="conversation",
            name="pdf_context_attached",
            field=models.BooleanField(default=False),
        ),
    ]

