from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from memberarea.apps.core.helpers import object_or_not_found
from .models import Tag
from .pagination import TagPagination
from .renderers import TagJSONRenderer
from .serializers import TagSerializer


class TagsAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TagSerializer
    pagination_class = TagPagination
    renderer_classes = (TagJSONRenderer, )

    def get(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data.get('tag'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TagSerializer
    renderer_classes = (TagJSONRenderer, )

    def get(self, request, pk):
        tag = object_or_not_found(Tag, pk)

        serializer = self.serializer_class(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        tag = object_or_not_found(Tag, pk)

        serializer = self.serializer_class(tag, data=request.data.get('tag'))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        tag = object_or_not_found(Tag, pk)

        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
