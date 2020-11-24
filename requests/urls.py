from django.conf.urls import url
from . import views
from django.contrib import admin

app_name = 'requests'

urlpatterns = [
    url(r'^$',views.ListRequests.as_view(),name='all'),
    url(r'^new/$',views.CreateRequest.as_view(),name='create'),
    url(r'posts/in/(?P<slug>[-\w]+)/$',views.Detail.as_view(),name='single'),
    # url(r'join/(?P<slug>[-\w]+)/$',views.JoinGroup.as_view(),name='join'),
    # url(r'leave/(?P<slug>[-\w]+)/$',views.LeaveGroup.as_view(),name='leave'),
    url(r'^admin/', admin.site.urls),
    # url(r'^<slug:slug>/', views.post_detail, name='post_detail'),
    url(r'^table/$',views.DCRTable.as_view(),name='table'),
]
