from django.contrib import admin
from django.urls import path, re_path
from base import views
from base import api_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="TF-IDF API",
      default_version='v1',
      description="Документация API TF/IDF",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('status', views.status_view),
    path('metrics', views.metrics_view),
    path('version', views.version_view),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('delete-account/', views.delete_user_view, name='delete_account'),
    path('collections/', api_views.collection_list),
    path('collections/<int:collection_id>/', api_views.collection_detail),
    path('collections/<int:collection_id>/statistics/', api_views.collection_statistics),
    path('collection/<int:collection_id>/<int:document_id>/add/', api_views.collection_add_doc),
    path('collection/<int:collection_id>/<int:document_id>/remove/', api_views.collection_remove_doc),
    path('documents/', api_views.document_list),
    path('documents/<int:document_id>/', api_views.document_content),
    path('documents/<int:document_id>/statistics/', api_views.document_statistics),
    path('documents/<int:document_id>/huffman/', api_views.document_huffman),
    path('delete-account/', views.delete_user_view, name='delete_account'),

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
