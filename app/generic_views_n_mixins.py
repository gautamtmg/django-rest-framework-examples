from rest_framework import generics
from rest_framework import mixins
from .models import Article
from .serializers import ArticelModelSerializer


class GenericAPIView(generics.GenericAPIView,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        ):
    serializer_class = ArticelModelSerializer
    queryset = Article.objects.all()

    lookup_field = 'id'


    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
        
            return self.list(request)

    def post(self, request):

        return self.create(request)

    def put(self, request, id = None):
        return self.update(request, id)

    def delete(self, request, id =None):
        return self.destroy(request, id)

