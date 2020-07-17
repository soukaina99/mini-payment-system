from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Payment API')

urlpatterns = [
                  path('docs/', schema_view),
                  path('', include('config.api_urls')),
                  path('admin/', include('config.admin_urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
