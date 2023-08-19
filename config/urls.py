from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .swagger import swaggerurlpatterns


def trigger_error(request):
    division_by_zero = 1 / 0  # noqa


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/common/", include("apps.common.urls")),
    path("api/driver/", include("apps.driver.urls")),
    path("api/order/", include("apps.order.urls")),
    path("api/v1/sentry/TriggerError/", trigger_error),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += swaggerurlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
