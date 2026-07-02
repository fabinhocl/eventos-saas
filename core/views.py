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
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from email.utils import formataddr
from .forms import EventForm, PublicRegistrationForm, RegistrationAdminForm, ParticipantForm
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

    if not participant.email:
        return

    access_url = f"{settings.SITE_URL}{reverse('participant_access', args=[registration.access_token])}"
    start_label = format_event_datetime(event.start_at) or 'A definir'
    end_label = format_event_datetime(event.end_at) or 'A definir'
    main_color = event.page_color or '#0d6c73'

    raw_logo_url = ''
    try:
        raw_logo_url = event.logo_src or ''
    except Exception:
        raw_logo_url = ''

    if raw_logo_url and raw_logo_url.startswith('http'):
        absolute_logo_url = raw_logo_url
    elif raw_logo_url:
        absolute_logo_url = f"{settings.SITE_URL}{raw_logo_url}"
    else:
        absolute_logo_url = ''

    context = {
        'registration': registration,
        'event': event,
        'participant': participant,
        'access_url': access_url,
        'start_label': start_label,
        'end_label': end_label,
        'main_color': main_color,
        'absolute_logo_url': absolute_logo_url,
    }

    subject = f'Confirmação de inscrição - {event.title}'
    text_body = render_to_string('email/registration_confirmation.txt', context)
    html_body = render_to_string('email/registration_confirmation.html', context)

    sender_name = event.title
    from_email = formataddr((sender_name, settings.DEFAULT_FROM_EMAIL))

    bcc_list = [settings.REGISTRATION_CONFIRMATION_BCC] if settings.REGISTRATION_CONFIRMATION_BCC else []

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[participant.email],
        bcc=bcc_list,
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
    nav_context = {'section': 'dashboard', 'page_title': 'Executive Overview', 'active_event': active_event, 'events': events}
    return render(request, 'core/dashboard.html', {'profile': profile, 'events': events, 'registrations': recent_registrations, 'active_event': active_event, 'active_registrations': active_registrations, 'event_stats': event_stats, 'sessions': sessions, 'nav_context': nav_context})


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
def participant_detail(request, participant_id):
    profile = get_organizer_profile(request.user)
    if not profile:
        return HttpResponseForbidden("Usuário sem vínculo com organização.")

    participant = get_object_or_404(Participant, pk=participant_id)

    latest_registration = (
        Registration.objects
        .select_related("event")
        .filter(participant=participant, event__tenant=profile.tenant)
        .order_by("-created_at")
        .first()
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            event_id = latest_registration.event.id if latest_registration else None
            participant.delete()
            messages.success(request, "Participante excluído com sucesso.")

            if event_id:
                return redirect("event_participants", event_id=event_id)
            return redirect("dashboard")

        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados do participante atualizados com sucesso.")
            return redirect("participant_detail", participant_id=participant.id)
        else:
            messages.error(request, "Corrija os campos destacados e tente novamente.")
    else:
        form = ParticipantForm(instance=participant)

    nav_context = {
        "section": "participants",
        "page_title": "Detalhes do participante",
        "active_event": latest_registration.event if latest_registration else None,
        "events": Event.objects.filter(tenant=profile.tenant).order_by("-created_at"),
    }

    context = {
        "profile": profile,
        "participant": participant,
        "form": form,
        "latest_registration": latest_registration,
        "nav_context": nav_context,
    }
    return render(request, "core/participant_detail.html", context)


@login_required
def event_participants_view(request, event_id):
    profile = get_organizer_profile(request.user)
    if not profile:
        return HttpResponseForbidden("Usuário sem vínculo com organização.")

    event = get_object_or_404(Event, id=event_id, tenant=profile.tenant)

    registrations = (
        event.registrations
        .select_related("participant", "event")
        .order_by("-created_at")
    )

    stats = {
        "total": registrations.count(),
        "confirmados": registrations.filter(status="confirmado").count(),
        "checkins": registrations.filter(status="confirmado").count(),
    }

    nav_context = {
        "section": "participants",
        "page_title": event.title,
        "active_event": event,
        "events": Event.objects.filter(tenant=profile.tenant).order_by("-created_at"),
    }

    return render(request, "core/event_participants.html", {
        "profile": profile,
        "event": event,
        "registrations": registrations,
        "stats": stats,
        "nav_context": nav_context,
    })



@login_required
def event_branding_view(request, event_id):
    profile = get_organizer_profile(request.user)
    if not profile:
        return HttpResponseForbidden('Usuário sem vínculo com organização.')

    event = get_object_or_404(Event, id=event_id, tenant=profile.tenant)

    if request.method == "POST":
        event.title = request.POST.get("title", event.title)
        event.location = request.POST.get("location", event.location)
        event.page_color = request.POST.get("page_color", event.page_color)
        event.background_color = request.POST.get("background_color", event.background_color)
        event.cta_label = request.POST.get("cta_label", event.cta_label)

        start_at = request.POST.get("start_at")
        end_at = request.POST.get("end_at")

        if start_at:
            parsed_start = parse_datetime(start_at)
            if parsed_start:
                event.start_at = parsed_start

        if end_at:
            parsed_end = parse_datetime(end_at)
            if parsed_end:
                event.end_at = parsed_end

        if request.FILES.get("logo"):
            event.logo_image = request.FILES["logo"]

        if request.FILES.get("cover_image"):
            event.banner_image = request.FILES["cover_image"]

        event.save()
        return redirect('event_branding', event_id=event.id)

    nav_context = {
        'section': 'branding',
        'page_title': 'Event Branding',
        'active_event': event,
        'events': Event.objects.filter(tenant=profile.tenant).order_by('-created_at'),
    }

    return render(request, 'core/event_branding.html', {
        'profile': profile,
        'event': event,
        'nav_context': nav_context,
    })

    
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
def participant_resend_email(request, registration_id):
    registration = get_object_or_404(
        Registration.objects.select_related("event", "participant"),
        pk=registration_id
    )

    if request.method == "POST":
        try:
            send_registration_confirmation(registration)
            messages.success(request, f"E-mail reenviado para {registration.participant.email}.")
        except Exception as e:
            messages.error(request, f"Erro ao reenviar e-mail: {e}")

    return redirect("event_participants", event_id=registration.event.id)


@login_required
def print_badge_view(request, registration_id):
    profile = get_organizer_profile(request.user)
    registration = get_object_or_404(Registration.objects.select_related('participant', 'event'), id=registration_id)
    if not profile or registration.event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')
    qr_payload, qr_mode_label = registration_qr_payload(registration)
    qr_code = qr_data_uri(qr_payload)
    return render(request, 'core/print_badge.html', {'registration': registration, 'qr_code': qr_code, 'qr_mode_label': qr_mode_label})


@property
def logo_src(self):
    if self.logo_image:
        return self.logo_image.url
    if self.logo_url:
        return self.logo_url
    return ''

@property
def banner_src(self):
    if self.banner_image:
        return self.banner_image.url
    if self.banner_url:
        return self.banner_url
    return ''

def public_event_view(request, slug):
    event = get_object_or_404(Event, slug=slug, public_active=True)
    context = {
        "event": event,
        "start_label": format_event_datetime(event.start_at),
        "end_label": format_event_datetime(event.end_at),
        "logo_src": event.logo_src,
        "banner_src": event.banner_src,
    }
    return render(request, "core/public_event.html", context)

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

    return render(request, 'core/public_registration.html', {
        'event': event,
        'form': form,
        'logo_src': event.logo_src,
        'banner_src': event.banner_src,
    })


def participant_access_view(request, token):
    registration = get_object_or_404(Registration.objects.select_related('event', 'participant'), access_token=token)

    return render(request, 'core/participant_access.html', {
        'registration': registration,
        'event': registration.event,
    })

@login_required
def event_checkin_view(request, event_id):
    profile = get_organizer_profile(request.user)
    event = get_object_or_404(Event, id=event_id)

    if not profile or event.tenant_id != profile.tenant_id:
        return HttpResponseForbidden('Acesso não permitido.')

    result = None

    if request.method == 'POST':
        raw_code = (request.POST.get('qr_payload') or '').strip()

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

    recent_registrations = (
        Registration.objects
        .select_related('participant')
        .filter(event=event)
        .order_by('-updated_at')[:10]
    )

    nav_context = {
        'section': 'checkin',
        'page_title': event.title,
        'active_event': event,
        'events': Event.objects.filter(tenant=profile.tenant).order_by('-created_at'),
    }

    return render(request, 'core/event_checkin.html', {
        'profile': profile,
        'event': event,
        'result': result,
        'recent_registrations': recent_registrations,
        'nav_context': nav_context,
    })

def debug_media_view(request):
    return HttpResponse(
        f"DEBUG={settings.DEBUG}<br>"
        f"MEDIA_URL={settings.MEDIA_URL}<br>"
        f"MEDIA_ROOT={settings.MEDIA_ROOT}"
    )   