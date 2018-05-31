from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from memberarea.apps.core.helpers import object_or_not_found
from .models import Clubhouse, Room, Defect
from .renderers import ClubhouseJSONRenderer, RoomJSONRenderer, DefectJSONRenderer
from .serializers import ClubhouseSerializer, RoomSerializer, DefectSerializer


class ClubhouseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Clubhouse.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ClubhouseSerializer
    renderer_classes = (ClubhouseJSONRenderer, )


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = RoomSerializer
    renderer_classes = (RoomJSONRenderer, )

    @action(methods=['GET'], detail=False, url_path='forclubhouse/(?P<clubhouseid>[^/.]+)')
    def forclubhouse(self, request, clubhouseid: int = None):
        clubhouse: Clubhouse = object_or_not_found(Clubhouse, clubhouseid)
        qs_for_clubhouse = self.get_queryset().filter(clubhouse=clubhouse)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_for_clubhouse)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)


class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DefectSerializer
    renderer_classes = (DefectJSONRenderer, )

    @action(methods=['GET'], detail=False)
    def notrepaired(self, request):
        qs_not_repaired = self.get_queryset().filter(repaired=False)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_not_repaired)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def markrepaired(self, request, pk=None):
        defect: Defect = object_or_not_found(Defect, pk)
        if request.method == 'POST':
            defect.repaired = True
        elif request.method == 'DELETE':
            defect.repaired = False

        defect.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
