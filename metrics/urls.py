from django.conf.urls import url
from metrics import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url('blocks/$', views.BlockView.as_view()),
    url('blocks/(?P<id>\d+)', views.BlockView.as_view()),
    url('chain/', views.ChainView.as_view()),
    url('transaction/', views.TransactionView.as_view()),
    url('sync/', views.SynchronizeView.as_view())
]
