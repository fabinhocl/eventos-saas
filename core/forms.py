from django import forms
from .models import Event, Registration, Participant

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'short_description', 'description', 'location', 'start_at', 'end_at', 'public_active',
            'banner_url', 'logo_url', 'banner_image', 'logo_image', 'page_color', 'background_color', 'text_color', 'cta_label', 'qr_mode'
        ]
        labels = {
            'banner_url': 'Banner por URL',
            'logo_url': 'Logo por URL',
            'banner_image': 'Arquivo do banner',
            'logo_image': 'Arquivo da logo',
            'page_color': 'Cor principal',
            'background_color': 'Cor de fundo',
            'text_color': 'Cor do texto',
            'cta_label': 'Texto do botão principal',
            'qr_mode': 'Modo do QR Code do crachá',
        }
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 6}),
            'page_color': forms.TextInput(attrs={'type': 'color'}),
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
        }
        help_texts = {
            'banner_image': 'Padrão recomendado: 1600x420 px em JPG ou PNG.',
            'logo_image': 'Padrão recomendado: 320x120 px com fundo transparente, preferencialmente PNG.',
        }

class PublicRegistrationForm(forms.Form):
    name = forms.CharField(label='Nome completo', max_length=180)
    email = forms.EmailField(label='E-mail')
    cpf = forms.CharField(label='CPF', max_length=14)
    phone = forms.CharField(label='Telefone / WhatsApp', max_length=40, required=False)
    company = forms.CharField(label='Empresa', max_length=180, required=False)
    role = forms.CharField(label='Cargo', max_length=180, required=False)

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_cpf(self):
        cpf = ''.join(filter(str.isdigit, self.cleaned_data['cpf']))
        if len(cpf) != 11:
            raise forms.ValidationError('Informe um CPF com 11 dígitos.')
        return cpf

class RegistrationAdminForm(forms.ModelForm):
    name = forms.CharField(label='Nome completo', max_length=180)
    email = forms.EmailField(label='E-mail')
    cpf = forms.CharField(label='CPF', max_length=14)
    phone = forms.CharField(label='Telefone / WhatsApp', max_length=40, required=False)
    company = forms.CharField(label='Empresa', max_length=180, required=False)
    role = forms.CharField(label='Cargo', max_length=180, required=False)

    class Meta:
        model = Registration
        fields = ['status', 'notes']
        labels = {'status': 'Status', 'notes': 'Observações'}
        widgets = {'notes': forms.Textarea(attrs={'rows': 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        participant = self.instance.participant
        self.fields['name'].initial = participant.name
        self.fields['email'].initial = participant.email
        self.fields['cpf'].initial = participant.cpf
        self.fields['phone'].initial = participant.phone
        self.fields['company'].initial = participant.company
        self.fields['role'].initial = participant.role

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = Participant.objects.filter(email=email).exclude(id=self.instance.participant_id)
        if qs.exists():
            raise forms.ValidationError('Já existe participante cadastrado com este e-mail.')
        return email

    def clean_cpf(self):
        cpf = ''.join(filter(str.isdigit, self.cleaned_data['cpf']))
        if len(cpf) != 11:
            raise forms.ValidationError('Informe um CPF com 11 dígitos.')
        qs = Participant.objects.filter(cpf=cpf).exclude(id=self.instance.participant_id)
        if qs.exists():
            raise forms.ValidationError('Já existe participante cadastrado com este CPF.')
        return cpf

    def save(self, commit=True):
        registration = super().save(commit=False)
        participant = registration.participant
        participant.name = self.cleaned_data['name']
        participant.email = self.cleaned_data['email']
        participant.cpf = self.cleaned_data['cpf']
        participant.phone = self.cleaned_data['phone']
        participant.company = self.cleaned_data['company']
        participant.role = self.cleaned_data['role']
        if commit:
            participant.save()
            registration.save()
        return registration
