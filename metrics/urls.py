from django.conf.urls import url
from metrics import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url('blocks/$', views.ListBlocksView.as_view()),
    url('blocks/(?P<pk>\d+)', views.ListBlocksView.as_view())

]