from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Book
from .serializers import BookSerializer
from django.views.decorators.csrf import csrf_exempt #it ignores csrf
from rest_framework.parsers import JSONParser
from rest_framework import status

@csrf_exempt
def bookListView(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializers = BookSerializer(books, many=True)
        return JsonResponse(serializers.data, safe=False)
    elif request.method == "POST":
        jsonData = JSONParser().parse(request)
        serializer = BookSerializer(data = jsonData)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)


@csrf_exempt
def bookDetailView(request, pk):

    try:
        book = Book.objects.get(pk = pk)

    except Book.DoesNotExist:
        return HttpResponse(status= 404)


    if request.method == "DELETE":
        book.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "GET":
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        jsonData = JSONParser().parse(request)
        serializer = BookSerializer(book, data = jsonData)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)
