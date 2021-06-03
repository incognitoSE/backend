from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views


schema_view = get_schema_view(
   openapi.Info(
      title="ML Estimator",
      default_version='V1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('HEstimator/', include('HouseEstimator.urls')),
    path('CEstimator/', include('CarEstimator.urls')),
    path('SEstimator/', include('SimCardEstimator.urls')),
    path('User/', include('User.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # re_path('^', include('django.contrib.auth.urls')),
    # re_path(r'^password_reset/$', auth_views.PasswordResetView, name='password_reset'),
    # re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView, name='password_reset_done'),
    # re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    # re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
]
