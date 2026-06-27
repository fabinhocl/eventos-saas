from io import BytesIO
import base64
import csv
import qrcode
from openpyxl import Workbook
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from .forms import EventForm, PublicRegistrationForm, RegistrationAdminForm
from .models import Event, OrganizerProfile, Participant, Registration


def get_organizer_profile(user):
    return OrganizerProfile.objects.select_related('tenant').filter(user=user).first()


def registration_vcard(registration):
    p = registration.participant
    participant_url = f"{settings.SITE_URL}{reverse('participant_access', args=[registration.access_token])}"
    lines = [
        'BEGIN:VCARD',
        'VERSION:3.0',
        f'FN:{p.name}',
    ]
    if p.email:
        lines.append(f'EMAIL:{p.email}')
    if p.phone:
        lines.append(f'TEL:{p.phone}')
    if p.company:
        lines.append(f'ORG:{p.company}')
    if p.role:
        lines.append(f'TITLE:{p.role}')
    lines.append(f'NOTE:{registration.event.title}')
    lines.append(f'URL:{participant_url}')
    lines.append('END:VCARD')
    return chr(10).join(lines)


def registration_checkin_payload(registration):
    return f"EVENTOSFLEX|CHECKIN|registration={registration.id}|token={registration.access_token}|event={registration.event_id}"


def registration_qr_payload(registration):
    mode = registration.event.qr_mode
    if mode == 'checkin':
        return registration_checkin_payload(registration), 'Check-in do participante'
    if mode == 'contact':
        return registration_vcard(registration), 'Contato do participante'
    return registration_vcard(registration), 'Contato + link da inscrição'


def qr_data_uri(text):
    img = qrcode.make(text)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('utf-8')


def format_event_datetime(value):
    if not value:
        return 'A definir'
    return timezone.localtime(value).strftime('%d/%m/%Y %H:%M')


def send_registration_confirmation(registration):
    event = registration.event
    participant = registration.participant
    access_url = f"{settings.SITE_URL}{reverse('participant_access', args=[registration.access_token])}"
    start_label = format_event_datetime(event.start_at)
    end_label = format_event_datetime(event.end_at)
    text_body = "\n".join([
        f"Olá, {participant.name}!",
        '',
        'Sua inscrição foi confirmada com sucesso.',
        f"Evento: {event.title}",
        f"Data de início: {start_label}",
        f"Data de encerramento: {end_label}",
        f"Local: {event.location or 'A definir'}",
        f"Empresa informada: {participant.company or 'Não informada'}",
        f"Link da sua inscrição: {access_url}",
        '',
        'Guarde este e-mail para consultar seus dados.',
    ])
    html_body = f"""
    <div style='font-family:Arial,sans-serif;background:#f5f3ee;padding:24px'>
      <div style='max-width:640px;margin:0 auto;background:#ffffff;border:1px solid #d9d9d9;border-radius:18px;overflow:hidden'>
        <div style='background:{event.page_color or '#0d6c73'};padding:20px 24px;color:#ffffff'>
          <h2 style='margin:0;font-size:24px'>Inscrição confirmada</h2>
          <p style='margin:8px 0 0 0'>{event.title}</p>
        </div>
        <div style='padding:24px'>
          <p>Olá, <strong>{participant.name}</strong>!</p>
          <p>Sua inscrição foi confirmada com sucesso.</p>
          <p><strong>Evento:</strong> {event.title}<br>
          <strong>Início:</strong> {start_label}<br>
          <strong>Fim:</strong> {end_label}<br>
          <strong>Local:</strong> {event.location or 'A definir'}<br>
          <strong>Empresa:</strong> {participant.company or 'Não informada'}</p>
          <p><a href='{access_url}' style='display:inline-block;padding:12px 18px;background:{event.page_color or '#0d6c73'};color:#ffffff;text-decoration:none;border-radius:999px'>Acessar minha inscrição</a></p>
          <p style='color:#666'>Guarde este e-mail para consultar seus dados e sua confirmação.</p>
        </div>
      </div>
    </div>
    """
    message = EmailMultiAlternatives(
        f'Confirmação de inscrição - {event.title}',
        text_body,
        settings.DEFAULT_FROM_EMAIL,
        [participant.email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)


def home_view(request):
    events = Event.objects.filter(public_active=True).order_by('-created_at')[:12]
    return render(request, 'core/home.html', {'events': events})


@login_required
def dashboard_view(request):
    profile = get_organizer_profile(request.user)
    if not profile:
        return HttpResponseForbidden('Usuário sem vínculo com organização.')
    events = Event.objects.filter(tenant=profile.tenant).order_by('-created_at')
    registrations = Registration.objects.filter(event__tenant=profile.tenant).select_related('participant', 'event').order_by('-created_at')
    active_event = events.first()
    event_id = request.GET.get('event')
    if event_id:
        active_event = events.filter(id=event_id).first() or active_event
    active_registrations = list(registrations.filter(event=active_event)[:20]) if active_event else []
    event_stats = {
        'total': len(active_registrations) if active_event else 0,
        'confirmados': sum(1 for r in active_registrations if r.status == 'confirmado'),
        'pendentes': sum(1 for r in active_registrations if r.status == 'pendente'),
        'cancelados': sum(1 for r in active_registrations if r.status == 'cancelado'),
    }
    sessions = [
        {'label': 'Abertura oficial', 'time': '09:00 - 09:30', 'place': active_event.location if active_event and active_event.location else 'Auditório principal'},
        {'label': 'Painel de conteúdo', 'time': '10:00 - 11:00', 'place': 'Sala 1'},
        {'label': 'Networking / Expo', 'time': '12:00 - 13:30', 'place': 'Foyer'},
    ] if active_event else []
    recent_registrations = list(registrations[:20])
    return render(request, 'core/dashboard.html', {'profile': profile, 'events': events, 'registrations': recent_registrations, 'active_event': active_event, 'active_registrations': active_registrations, 'event_stats': event_stats, 'sessions': sessions})


@login_required
def event_create_view(request):
    profile = get_organizer_profile(request.user)
    if not profile:
        return HttpResponseForbidden('Usuário sem vínculo com organização.')
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.tenant = profile.tenant
        event.save()
        messages.success(request, 'Evento criado com sucesso.')
        return redirect('event_detail', event_id=event.id)
    return render(request, 'core/event_form.html', {'form': form, 'profile': profile, 'mode': 'create'})


@login_required
def event_overview_view(request, event_id):
    profile = get_organizer_profile(request.user)
    event = get_object_or_404(Event, id=event_id)
    if not profile or event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    registrations = event.registrations.select_related('participant').order_by('-created_at')
    stats = {
        'total': registrations.count(),
        'confirmados': registrations.filter(status='confirmado').count(),
        'pendentes': registrations.filter(status='pendente').count(),
        'cancelados': registrations.filter(status='cancelado').count(),
    }
    return render(request, 'core/event_overview.html', {'profile': profile, 'event': event, 'stats': stats})


@login_required
def event_participants_view(request, event_id):
    profile = get_organizer_profile(request.user)
    event = get_object_or_404(Event, id=event_id)
    if not profile or event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    status_filter = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()
    registrations = event.registrations.select_related('participant').order_by('-created_at')
    if status_filter:
        registrations = registrations.filter(status=status_filter)
    if query:
        registrations = registrations.filter(participant__name__icontains=query) | event.registrations.filter(participant__email__icontains=query)
    return render(request, 'core/event_participants.html', {
        'profile': profile,
        'event': event,
        'registrations': registrations,
        'status_filter': status_filter,
        'query': query,
    })


@login_required
def event_branding_view(request, event_id):
    profile = get_organizer_profile(request.user)
    event = get_object_or_404(Event, id=event_id)
    if not profile or event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        updated = form.save()
        messages.success(request, 'Hotpage atualizada com sucesso.')
        return redirect('event_branding', event_id=updated.id)
    return render(request, 'core/event_branding.html', {'profile': profile, 'event': event, 'form': form})


@login_required
def export_event_csv_view(request, event_id):
    profile = get_organizer_profile(request.user)
    event = get_object_or_404(Event, id=event_id)
    if not profile or event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="inscritos-evento-{event.id}.csv"'
    response.write('﻿')
    writer = csv.writer(response)
    writer.writerow(['Nome', 'E-mail', 'CPF', 'Telefone', 'Empresa', 'Cargo', 'Status'])
    for reg in event.registrations.select_related('participant').all():
        p = reg.participant
        writer.writerow([p.name, p.email, p.cpf, p.phone, p.company, p.role, reg.status])
    return response


@login_required
def export_event_xlsx_view(request, event_id):
    profile = get_organizer_profile(request.user)
    event = get_object_or_404(Event, id=event_id)
    if not profile or event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    wb = Workbook()
    ws = wb.active
    ws.title = 'Inscritos'
    ws.append(['Nome', 'E-mail', 'CPF', 'Telefone', 'Empresa', 'Cargo', 'Status'])
    for reg in event.registrations.select_related('participant').all():
        p = reg.participant
        ws.append([p.name, p.email, p.cpf, p.phone, p.company, p.role, reg.status])
    output = BytesIO()
    wb.save(output)
    response = HttpResponse(output.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="inscritos-evento-{event.id}.xlsx"'
    return response


@login_required
def registration_admin_view(request, registration_id):
    profile = get_organizer_profile(request.user)
    registration = get_object_or_404(Registration.objects.select_related('participant', 'event'), id=registration_id)
    if not profile or registration.event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    form = RegistrationAdminForm(request.POST or None, instance=registration)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cadastro atualizado com sucesso.')
        return redirect('registration_admin', registration_id=registration.id)
    return render(request, 'core/registration_admin.html', {'registration': registration, 'form': form, 'profile': profile})


@login_required
def resend_confirmation_view(request, registration_id):
    profile = get_organizer_profile(request.user)
    registration = get_object_or_404(Registration.objects.select_related('participant', 'event'), id=registration_id)
    if not profile or registration.event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    try:
        send_registration_confirmation(registration)
        messages.success(request, f'E-mail reenviado para {registration.participant.email}.')
    except Exception as exc:
        messages.error(request, f'Falha no envio: {exc}')
    return redirect('registration_admin', registration_id=registration.id)


@login_required
def print_badge_view(request, registration_id):
    profile = get_organizer_profile(request.user)
    registration = get_object_or_404(Registration.objects.select_related('participant', 'event'), id=registration_id)
    if not profile or registration.event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    qr_payload, qr_mode_label = registration_qr_payload(registration)
    qr_code = qr_data_uri(qr_payload)
    return render(request, 'core/print_badge.html', {'registration': registration, 'qr_code': qr_code, 'qr_mode_label': qr_mode_label})


def public_event_view(request, slug):
    event = get_object_or_404(Event, slug=slug, public_active=True)
    return render(request, 'core/public_event.html', {'event': event, 'start_label': format_event_datetime(event.start_at), 'end_label': format_event_datetime(event.end_at)})


def public_registration_view(request, slug):
    event = get_object_or_404(Event, slug=slug, public_active=True)
    form = PublicRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        cpf = form.cleaned_data['cpf']
        participant = Participant.objects.filter(email=email).first() or Participant.objects.filter(cpf=cpf).first()
        if participant:
            if participant.email != email and Participant.objects.filter(email=email).exclude(id=participant.id).exists():
                form.add_error('email', 'Já existe outro participante cadastrado com este e-mail.')
            if participant.cpf != cpf and Participant.objects.filter(cpf=cpf).exclude(id=participant.id).exists():
                form.add_error('cpf', 'Já existe outro participante cadastrado com este CPF.')
            if not form.errors:
                participant.name = form.cleaned_data['name']
                participant.email = email
                participant.cpf = cpf
                participant.phone = form.cleaned_data['phone']
                participant.company = form.cleaned_data['company']
                participant.role = form.cleaned_data['role']
                participant.save()
        else:
            if Participant.objects.filter(email=email).exists():
                form.add_error('email', 'Já existe outro participante cadastrado com este e-mail.')
            if Participant.objects.filter(cpf=cpf).exists():
                form.add_error('cpf', 'Já existe outro participante cadastrado com este CPF.')
            if not form.errors:
                participant = Participant.objects.create(
                    name=form.cleaned_data['name'],
                    email=email,
                    cpf=cpf,
                    phone=form.cleaned_data['phone'],
                    company=form.cleaned_data['company'],
                    role=form.cleaned_data['role'],
                )
        if not form.errors:
            existing_registration = Registration.objects.filter(event=event, participant=participant).first()
            if existing_registration:
                messages.info(request, 'Este participante já estava inscrito neste evento.')
                return redirect('participant_access', token=existing_registration.access_token)
            registration = Registration.objects.create(event=event, participant=participant)
            try:
                send_registration_confirmation(registration)
                messages.success(request, 'Inscrição confirmada. Enviamos um e-mail com o link para consultar seu cadastro.')
            except Exception as exc:
                messages.error(request, f'Inscrição salva, mas houve falha no envio do e-mail: {exc}')
            return redirect('participant_access', token=registration.access_token)
    return render(request, 'core/public_registration.html', {'event': event, 'form': form})


def participant_access_view(request, token):
    registration = get_object_or_404(Registration.objects.select_related('participant', 'event'), access_token=token)
    return render(request, 'core/participant_access.html', {'registration': registration})


@login_required
def event_checkin_view(request, event_id):
    profile = get_organizer_profile(request.user)
    event = get_object_or_404(Event, id=event_id)
    if not profile or event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    result = None
    if request.method == 'POST':
        raw_code = (request.POST.get('qr_content') or '').strip()
        if 'EVENTOSFLEX|CHECKIN|' not in raw_code:
            messages.error(request, 'QR Code inválido para check-in.')
        else:
            try:
                parts = dict(piece.split('=', 1) for piece in raw_code.split('|')[2:])
                registration = Registration.objects.select_related('participant', 'event').get(
                    id=int(parts['registration']),
                    event_id=int(parts['event']),
                    access_token=parts['token'],
                )
                if registration.event_id != event.id:
                    messages.error(request, 'Este QR pertence a outro evento.')
                else:
                    registration.status = 'confirmado'
                    stamp = timezone.now().strftime('%d/%m/%Y %H:%M')
                    registration.notes = ((registration.notes or '') + f"\nCheck-in registrado em {stamp}").strip()
                    registration.save()
                    result = registration
                    messages.success(request, f'Check-in realizado para {registration.participant.name}.')
            except Exception:
                messages.error(request, 'Não foi possível validar o QR Code informado.')
    return render(request, 'core/event_checkin.html', {'profile': profile, 'event': event, 'result': result})
