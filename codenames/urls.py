"""codenames URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django_registration.backends.one_step.views import RegistrationView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/',
         auth_views.LoginView.as_view(template_name='django_registration/login.html'),
         name='login'),
    path('register/', RegistrationView.as_view(success_url='/')),
    path('', include('django_registration.backends.one_step.urls')),
    # path('accounts/', include('django_registration.backends.one_step.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('guess/', views.guess, name='guess'),
    path('give/', views.give, name='give'),
    path('comment/', views.comment, name='comment'),
    # url(r'^comment/(?P<comment_id>\d+)$', views.comment, name='comment'),
    path('comment/<int:comment_id>', views.comment, name='comment'),
    # url(r'^game/(?P<unique_id>\w+)$', views.game, name='game'),
    path('game/<str:unique_id>', views.game, name='game'),
    # url(r'^waiting/(?P<user_id>\w+)$', views.waiting, name='waiting'),
    path('waiting/<str:user_id>', views.waiting, name='waiting'),
    path('create/', login_required(views.GameCreate.as_view()), name='create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
#         ('document_root', settings.STATIC_ROOT)),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
