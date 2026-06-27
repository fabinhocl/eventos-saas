from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_event_banner_image_event_logo_image_participant_cpf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='qr_mode',
            field=models.CharField(choices=[('contact', 'Salvar contato'), ('checkin', 'Check-in'), ('both', 'Contato + check-in')], default='both', max_length=20),
        ),
    ]
