from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_event_qr_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizerprofile',
            name='role',
            field=models.CharField(
                choices=[('admin', 'Administrador'), ('basic', 'Operação básica')],
                default='admin',
                max_length=20,
            ),
        ),
    ]