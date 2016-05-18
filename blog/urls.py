from django.conf.urls import url,include
from blog import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^article/$', views.get_article, name='article'),
    url(r'^comment/post/$', views.comment_post, name='comment_post'),
    url(r'^logout$', views.do_logout, name='logout'),
    url(r'^reg', views.do_reg, name='reg'),
    url(r'^login', views.do_login, name='login'),
    url(r'^catalog/$', views.catalog, name='catalog'),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^resume/$', views.resume, name='resume'),
]
