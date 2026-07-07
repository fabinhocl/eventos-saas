from django import forms
from django.contrib.auth.models import User
from .models import Event, Registration, Participant, OrganizerProfile

class OrganizerUserCreateForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150)
    last_name = forms.CharField(label='Sobrenome', max_length=150, required=False)
    username = forms.CharField(label='Usuário', max_length=150)
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Senha inicial', widget=forms.PasswordInput)
    role = forms.ChoiceField(label='Perfil', choices=OrganizerProfile.ROLE_CHOICES)
    allowed_events = forms.ModelMultipleChoiceField(
        label='Eventos liberados',
        queryset=Event.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, tenant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tenant:
            self.fields['allowed_events'].queryset = Event.objects.filter(
                tenant=tenant
            ).order_by('-created_at')
            
    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Já existe um usuário com esse login.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com esse e-mail.')
        return email
    

class OrganizerUserEditForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150)
    last_name = forms.CharField(label='Sobrenome', max_length=150, required=False)
    username = forms.CharField(label='Usuário', max_length=150)
    email = forms.EmailField(label='E-mail')
    role = forms.ChoiceField(label='Perfil', choices=OrganizerProfile.ROLE_CHOICES)
    allowed_events = forms.ModelMultipleChoiceField(
        label='Eventos liberados',
        queryset=Event.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, tenant=None, instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        if tenant:
            self.fields['allowed_events'].queryset = Event.objects.filter(
                tenant=tenant
            ).order_by('-created_at')

        # Pré-preenche os dados a partir do OrganizerProfile e User
        if instance is not None:
            user = instance.user
            self.initial.setdefault('first_name', user.first_name)
            self.initial.setdefault('last_name', user.last_name)
            self.initial.setdefault('username', user.username)
            self.initial.setdefault('email', user.email)
            self.initial.setdefault('role', instance.role)
            self.initial.setdefault('allowed_events', instance.allowed_events.all())

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        qs = User.objects.filter(username=username)
        # permite o mesmo username do próprio usuário
        if self.initial.get('username'):
            qs = qs.exclude(username=self.initial['username'])
        if qs.exists():
            raise forms.ValidationError('Já existe um usuário com esse login.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        qs = User.objects.filter(email=email)
        if self.initial.get('email'):
            qs = qs.exclude(email=self.initial['email'])
        if qs.exists():
            raise forms.ValidationError('Já existe um usuário com esse e-mail.')
        return email


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


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "cpf", "phone", "company", "role"]