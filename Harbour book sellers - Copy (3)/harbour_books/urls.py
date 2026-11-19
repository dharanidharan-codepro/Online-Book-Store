
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views as account_views

admin.site.site_header = 'Harbour Books Admin'
admin.site.site_title = 'Harbour Books'

handler404 = 'catalog.views.page_not_found'
handler500 = 'catalog.views.server_error'
handler403 = 'catalog.views.permission_denied'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('accounts/', include('accounts.urls')),
    path('login/staff/', account_views.staff_login, name='staff_login'),
    path('manage/', account_views.dashboard, name='manage_dashboard'),
    path('', include('cart.urls')),
    path('', include('newsletter.urls')),
    path('', include('ai_summary.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
