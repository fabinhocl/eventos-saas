from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('organizacao/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('organizacao/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('organizacao/', views.dashboard_view, name='dashboard'),
    path('organizacao/eventos/novo/', views.event_create_view, name='event_create'),
    path('organizacao/eventos/<int:event_id>/', views.event_overview_view, name='event_detail'),
    path('organizacao/eventos/<int:event_id>/participantes/', views.event_participants_view, name='event_participants'),
    path('organizacao/eventos/<int:event_id>/branding/', views.event_branding_view, name='event_branding'),
    path('organizacao/eventos/<int:event_id>/checkin/', views.event_checkin_view, name='event_checkin'),
    path('organizacao/eventos/<int:event_id>/exportar-csv/', views.export_event_csv_view, name='export_event_csv'),
    path('organizacao/eventos/<int:event_id>/exportar-xlsx/', views.export_event_xlsx_view, name='export_event_xlsx'),
    path('organizacao/inscricao/<int:registration_id>/', views.registration_admin_view, name='registration_admin'),
    path('organizacao/inscricao/<int:registration_id>/reenviar-email/', views.resend_confirmation_view, name='resend_confirmation'),
    path('organizacao/inscricao/<int:registration_id>/etiqueta/', views.print_badge_view, name='print_badge'),
    path('e/<slug:slug>/', views.public_event_view, name='public_event'),
    path('e/<slug:slug>/inscricao/', views.public_registration_view, name='public_registration'),
    path('minha-inscricao/<uuid:token>/', views.participant_access_view, name='participant_access'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
