from django.urls import path
from .views import article_list, article_detail
from .api_view_decorator_views import article_list_api_view, detail_api_view


urlpatterns = [
    path('article/', article_list),
    path('detail/<int:pk>/', article_detail),
    path('article-api-view/', article_list_api_view),
    path('detail-api-view/<int:pk>/', detail_api_view)

]