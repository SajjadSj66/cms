from django.urls import path
from . import views
from .views import BlogListView, BlogDetailView, SharePost

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>/', BlogDetailView.as_view(), name='blog-item'),
    path('d/<int:pk>/', BlogDetailView.as_view(), name='blog-item'),
    path('categories', views.categories_view),
    path('share/<int:pk>', views.SharePost.as_view(), name='share-post')
]
