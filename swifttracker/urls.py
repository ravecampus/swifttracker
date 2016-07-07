from django.conf.urls.static import static
from django.contrib.auth import views as login
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from accounts.views import *

urlpatterns = [
    # Examples:
    url(r'^$', 'accounts.views.home_view', name="home"),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$',LoginView.as_view(), name='login'),
    url(r'^logout/$', 'accounts.views.logout_view', name='logout'),
    url(r'^dashboard/$',DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/edit_profile/$',EditProfileView.as_view(), name='edit_profile'),
    url(r'^dashboard/projects/(?P<project_id>\d+)/$', 'accounts.views.project_view', name="project_detail"),
    url(r'^dashboard/projects/add_report/(?P<project_id>\d+)/$', 'accounts.views.add_report_view', name="add_report"),
    url(r'^dashboard/projects/edit_report/(?P<project_id>\d+)/(?P<report_id>\d+)/$', 'accounts.views.edit_report_view', name="edit_report"),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


