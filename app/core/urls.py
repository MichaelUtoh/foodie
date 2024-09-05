import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from accounts.api import UserDetailViewSet, UserLoginAPIView, UserRegisterAPIView
from payments.api import PaymentViewSet
from .views import ping

schema_view = get_schema_view(
    openapi.Info(
        title="NRI",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()

urlpatterns = router.urls
urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        # re_path(
        #     r"^swagger(?P<format>\.json|\.yaml)$",
        #     schema_view.without_ui(cache_timeout=0),
        #     name="schema-json",
        # ),
        # re_path(w
        #     r"^swagger/$",
        #     schema_view.with_ui("swagger", cache_timeout=0),
        #     name="schema-swagger-ui",
        # ),
        # re_path(
        #     r"^redoc/$",
        #     schema_view.with_ui("redoc", cache_timeout=0),
        #     name="schema-redoc",
        # ),
        re_path(r"auth/register/", UserRegisterAPIView.as_view(), name="register"),
        re_path(r"auth/login/", UserLoginAPIView.as_view(), name="login"),
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
