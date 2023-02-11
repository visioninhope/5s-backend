from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from apps.router import routes
from .views import RegisterView, GetHost, setcookie, getcookie

# auth/register
urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
# main routes
urlpatterns += [
    path("admin/", admin.site.urls),
    path("api/", include(routes)),
    path("get_ip/", GetHost.as_view()),
]
# config routes
urlpatterns += [
    path("scookie", setcookie),
    path("gcookie", getcookie),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
