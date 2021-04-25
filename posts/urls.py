from . import views
from django.conf import Path

app_name = 'posts'

urlpatterns = [
    Path("",views.PostList.as_view(),name='all'),
    Path("by/<username>/",views.UserPost.as_view(),name='for_user'),
    Path("by/<username>/<int:pk>/",views.PostDetail.as_view(),name='single'),
    Path("new/",views.Createpost.as_view(),name='create'),
    Path("delete/<int: pk>/",views.DeletePost.as_view(),name='delete'),
]