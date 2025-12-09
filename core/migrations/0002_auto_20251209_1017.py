from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # make sure this matches your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='booking',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
