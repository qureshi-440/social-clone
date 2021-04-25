from django.conf import Path
from . import views

app_name = "groups"

urlpatterns = [
    Path("",views.ListGroup.as_view(),name='all'),
    Path("new/",views.CreateGroup.as_view(),name='create'),
    Path("post/<slug>/",views.SingleGroup.as_view(),name='single'),
    Path("join/<slug>/",views.Joingroup.as_view(),name='join'),
    Path('leave/<slug>/',views.leaveGroup.as_view(),name='leave'),
]