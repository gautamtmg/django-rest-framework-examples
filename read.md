# Django REST framework

### To install django REST framework

> pip install djangorestframework

### Goto settings.py and add 'rest_framework' in installed apps
```python
INSTALLED_APPS = [
   ....
    'rest_framework'
]
```
 
### Make a model
```python
from django.db.models.base import Model

class Book(models.Model):
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    price = models.IntegerField(default=0)
```

#### After making we need to make serializers, which helps to convert python objects into datatype that is understandable by javascript (JSON)
> serializes.py
```python
from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=80)
    author = serializers.CharField(max_length=80)
    price = serializers.IntegerField(default=0)
```


### To response a JSON file
> views.py
```python
from django.http import JsonResponse

def bookListView(request):

    return JsonResponse({"title": " Book Title Here"})
```

### Now with serializers
> views.py
```python
from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer

def bookListView(request):
    books = Book.objects.all()
    serializers = BookSerializer(books, many=True)
    return JsonResponse(serializers.data, safe=False)
```
> In order to allow non-dict objects to be serialized set the safe parameter to False.
> Here serializer converts python object inot Json and serializers.data is in string fromat so we need to add safe=False

### To handle POST request
> view.py
```python
from django.http import JsonResponse
from .models import Book
from .serializers import BookSerializer
from django.views.decorators.csrf import csrf_exempt #it ignores csrf
from rest_framework.parsers import JSONParser

@csrf_exempt
def bookListView(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializers = BookSerializer(books, many=True)
        return JsonResponse(serializers.data, safe=False)
    elif request.method == "POST":
        jsonData = JSONParser().parse(request)
        serializers = BookSerializer(data = jsonData)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, safe=False)
        else:
            return JsonResponse(serializers.errors, safe=False)
```
> In HTTP request, we receive data as string. JSONparser().parse() helps to convert JSON content into python data types based on Content-Type header.

### Make create() method inside the serializer Class
> serializer.save() method call create() function in serializer Class (BookSerializer)
> serializers.py

```python
from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=80)
    author = serializers.CharField(max_length=80)
    price = serializers.IntegerField(default=0)

    def create(self, validated__data):  # this validated_data comes in dictionary form
        return Book.objects.create(**validated__data)

```

### To GET, Update and Delete particular one
> views.py
```python

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
```

#### For PUT request, create update() function in serializer class
> serializers.py
```python
class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=80)
    author = serializers.CharField(max_length=80)
    price = serializers.IntegerField(default=0)

    def create(self, validated_data):  # this validated_data comes in dictionary form
        return Book.objects.create(**validated_data)


    def update(self, instance, validated_data):
        newBook = Book(**validated_data)
        newBook.id = instance.id
        newBook.save()
        return newBook

```

## Now using rest_framework Response, decorators --> api_view()
```
request.POST  # Only handles form data.  Only works for 'POST' method.
request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
```
> views.py
```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def bookListView(request):
    if request.method == "GET":
        books = Book.objects.all()
        serializers = BookSerializer(books, many=True)
        return Response(serializers.data)
    elif request.method == "POST":
        # here we don't need to parse the data using JSONParser().parse(), we use request.data directly
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def bookDetailView(request, pk):

    try:
        book = Book.objects.get(pk = pk)

    except Book.DoesNotExist:
        return Response(status= 404)


    if request.method == "DELETE":
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "GET":
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = BookSerializer(book, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

```

## Using ModelSerializer
> serializers.py
```python
from django.db.models import fields
from app.models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book

        # fields = ['tittle', 'author']     Only selected fields data will be shown
        # Whicf field you wan to serialize
        fields = '__all__'
```

## Class Based View
| Function Based View  | Class Based View |
| -------------------- | ---------------  |
| def bookView():      | class BookView() |
| if get:              | get()            |
| if post:             | post()           |
| if put:              | put()            |
| if delete:           | delete()         |


```python
...
from django.http import Http404

# classed Based View
class BookListView(APIView):
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class BookDetailView(APIView):

    def get_book(self,pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_book(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk):
        book = self.get_book(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        book = self.get_book(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```


# Nested Serializer

> models.py
```python
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    price = models.IntegerField(default=0)


    def __str__(self):
        return self.title
```

> serializers.py
```python
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Book, Category



class CategorySerializer(serializers.ModelSerializer):
    # books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Book
        fields = "__all__"
```