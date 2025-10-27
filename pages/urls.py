
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.landing, name="landing"),

    path("signup/", views.signup_view, name="signup"),


    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),

    path("contact/", views.contact, name="contact"),

    path("about",views.about,name="about"),

    # pages/urls.py
    path('profile/', views.profile, name='profile'),


    # Password Reset URLs
    path("reset_password/",
         auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name="reset_password"),

    path("reset_password_sent/",
         auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="reset_password_confirm.html"),
         name="password_reset_confirm"),

    path("reset_password_complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
         name="password_reset_complete"),

    path('dashboard1/', views.dashboard1, name='dashboard1'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),


    path('profile/<str:username>/', views.profile, name='profile'),
    #path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('calendar/', views.calendar_view, name='calendar'),
    path('events/', views.events_json, name='events_json'),
    path('add-event/', views.add_event, name='add_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),

   path('dashboard/', views.dashboard, name='dashboard'),
   path('delete/<int:website_id>/', views.delete_website, name='delete_website'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)