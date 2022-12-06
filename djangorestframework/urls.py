"""djangorestframework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import bookListView, bookDetailView
from using_decorators.views import BookListView as book, BookDetailView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/book/', bookListView),
    path('api/book/<int:pk>', bookDetailView),
    # path('api/book/using-decorator/', book),
    # path('api/book/using-decorator/<int:pk>', bookDetail),
    path('api/book/serializer-class/', book.as_view()),
    path('api/book/serializer-class/<int:pk>', BookDetailView.as_view()),
    path('api/', include('nestedserializer.urls')),

]
