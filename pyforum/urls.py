from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('pyforum.views',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'forum_list', name='forum_list'),
    url(r'^forum/(?P<forum_id>\d+)/$', 'forum_detail', name='forum_detail'),
    url(r'^forum/(?P<forum_id>\d+)/compose/$', 'compose', name='compose'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'thread_detail', name='thread_detail'),
    url(r'^user/(?P<user_id>\d+)/$', 'user_detail', name='user_detail'),
)
