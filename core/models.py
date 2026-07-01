import uuid
from django.contrib.auth.models import User
from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    contact_email = models.EmailField()
    primary_color = models.CharField(max_length=20, blank=True, default='#0d6c73')
    logo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='organizers')

    def __str__(self):
        return f'{self.user.username} - {self.tenant.name}'

class Event(models.Model):
    QR_MODE_CHOICES = [('contact', 'Salvar contato'), ('checkin', 'Check-in'), ('both', 'Contato + check-in')]
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='events')
    title = models.CharField('Título', max_length=180)
    slug = models.SlugField(unique=True)
    short_description = models.CharField('Descrição curta', max_length=255)
    description = models.TextField('Descrição', blank=True)
    location = models.CharField('Local', max_length=180, blank=True)
    start_at = models.DateTimeField('Início', null=True, blank=True)
    end_at = models.DateTimeField('Fim', null=True, blank=True)
    public_active = models.BooleanField('Evento público ativo', default=True)
    banner_url = models.URLField('Banner por URL', blank=True)
    logo_url = models.URLField('Logo por URL', blank=True)
    banner_image = models.ImageField('Arquivo do banner', upload_to='event_banners/', blank=True, null=True)
    logo_image = models.ImageField('Arquivo da logo', upload_to='event_logos/', blank=True, null=True)
    page_color = models.CharField('Cor principal', max_length=20, blank=True, default='#0d6c73')
    background_color = models.CharField('Cor de fundo', max_length=20, blank=True, default='#f5f3ee')
    text_color = models.CharField('Cor do texto', max_length=20, blank=True, default='#222222')
    cta_label = models.CharField('Texto do botão principal', max_length=60, blank=True, default='Fazer inscrição')
    qr_mode = models.CharField('Modo do QR Code', max_length=20, choices=QR_MODE_CHOICES, default='both')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def banner_src(self):
        if self.banner_image:
            return self.banner_image.url
        return self.banner_url

    @property
    def logo_src(self):
        if self.logo_image:
            return self.logo_image.url
        return self.logo_url

    def __str__(self):
        return self.title

    @property
    def qr_mode_label(self):
        return dict(self.QR_MODE_CHOICES).get(self.qr_mode, 'Contato + check-in')

class Participant(models.Model):
    name = models.CharField('Nome completo', max_length=180)
    email = models.EmailField('E-mail', unique=True)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    phone = models.CharField('Telefone / WhatsApp', max_length=40, blank=True)
    company = models.CharField('Empresa', max_length=180, blank=True)
    role = models.CharField('Cargo', max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='registrations')
    access_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField('Status', max_length=30, default='confirmado')
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'participant')

    def __str__(self):
        return f'{self.participant.name} - {self.event.title}'
