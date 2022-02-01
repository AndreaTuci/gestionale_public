from django.contrib import admin
from django.urls import path, include
from django.conf import settings
# from django.contrib.auth.views import logout
from django.conf.urls.static import static
from django.contrib.auth import logout
from core.views import handler500 as error500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('social_django.urls', namespace='social')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('amministrazione/', include('amministrazione.urls')),
    path('anagrafica/', include('anagrafica.urls')),
    path('frequenze/', include('frequenze.urls')),
    path('captcha/', include('captcha.urls')),
]

handler500 = error500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)