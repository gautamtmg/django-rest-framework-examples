from .models import Article
from rest_framework import serializers


# class BookSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=80)
#     author = serializers.CharField(max_length=80)
#     price = serializers.IntegerField(default=0)

#     def create(self, validated_data):  # this validated_data comes in dictionary form
#         return Book.objects.create(**validated_data)


#     def update(self, instance, validated_data):
#         newBook = Book(**validated_data)
#         newBook.id = instance.id
#         newBook.save()
#         return newBook


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=80)
    author = serializers.CharField(max_length=80)
    email = serializers.EmailField(max_length=100)
    date = serializers.DateTimeField()

    def create(self, validated_data):
        
        return Article.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.email = validated_data.get('email', instance.email)
        instance.date = validated_data.get('date', instance.date)

        instance.save()

        return instance

        
