from django.conf.urls import patterns, url

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
    url(r'^forum/(?P<forum_id>\d+)/compose/$', 'compose_thread',
        name='compose_thread'),
    url(r'^thread/(?P<thread_id>\d+)/$', 'thread_detail', name='thread_detail'),
    url(r'^thread/(?P<thread_id>\d+)/compose/$', 'compose_post',
        name='compose_post'),
    url(r'^save_post/$', 'save_post', name='save_post'),
    url(r'^post/(?P<post_id>\d+)/edit/$', 'edit_post', name='edit_post'),
    url(r'^post/(?P<post_id>\d+)/delete/$', 'delete_post', name="delete_post"),
    url(r'^user/(?P<user_id>\d+)/$', 'user_detail', name='user_detail'),
    url(r'^sign_up/$', 'sign_up', name='sign_up'),
    url(r'^save_user/$', 'save_user', name='save_user'),
    url(r'^sign_in/$', 'sign_in', name='sign_in'),
    url(r'^auth_user/$', 'auth_user', name='auth_user'),
    url(r'^sign_out/$', 'sign_out', name='sign_out'),
)
