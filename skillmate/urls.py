from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.courses import views as course_views

admin.site.site_header = "SkillMate Admin"
admin.site.site_title = "SkillMate"
admin.site.index_title = "Boshqaruv Paneli"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', course_views.home, name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('courses/', include('apps.courses.urls')),
    path('lms/', include('apps.lms.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
