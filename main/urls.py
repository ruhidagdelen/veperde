from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from . import views

app_name = 'main'

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^oyunlar/$', views.acts, name='acts'),
                  url(r'^oyunekle/$', views.addAct, name='addAct'),
                  url(r'^oyunlar/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
                  url(r'^oyunlar/duzenle/(?P<pk>[0-9]+)/$', views.changeAct, name='changeAct'),
                  url(r'^elestiriler/$', views.critic, name='critic'),
                  url(r'^elestiriler/(?P<pk>[0-9]+)/$', views.critic_detail, name='critic_detail'),
                  url(r'^elestiriler/(?P<pk>[0-9]+)/sil/$', views.deleteCritic, name='deleteCritic'),
                  url(r'^elestiriler/guncelle/(?P<pk>[0-9]+)/$', views.updateCritic, name='updateCritic'),
                  url(r'^elestiriler/(?P<pk>[0-9]+)/yorumsil/', views.deleteComment, name='deleteComment'),
                  url(r'^yaziekle/$', views.addCritic, name='addCritic'),
                  url(r'^yazarol/$', views.addUser, name='addUser'),
                  url(r'^topluluk/(?P<pk>[0-9]+)/$', views.communityDetail, name='communityDetail'),
                  url(r'^kullanici/$', views.profile, name='profile'),
                  url(r'^elestirionayla/$', views.approveCritic, name='approveCritic'),
                  url(r'^onayla/(?P<pk>[0-9]+)$', views.approveC, name='approveC'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
