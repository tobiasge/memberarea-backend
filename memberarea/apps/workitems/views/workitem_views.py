from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from memberarea.apps.authentication.models import User
from memberarea.apps.core.helpers import object_or_not_found
from memberarea.apps.tags.models import Tag
from ..models import Workitem, WorkitemAssignment
from ..renderers import WorkitemJSONRenderer, WorkitemAssignmentJSONRenderer
from ..serializers import WorkitemSerializer, WorkitemAssignmentSerializer


class WorkitemViewSet(viewsets.ModelViewSet):
    """

    mine:
    Load a list of workitems that are assigned to the current user and not done

    published:
    Load a list of workitems that are published user and not done

    assign:
    Manage user assignment for a workitem
    """
    queryset = Workitem.objects.all()
    serializer_class = WorkitemSerializer
    renderer_classes = (WorkitemJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        serializer = self.serializer_class(data=request.data.get('workitem'))
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False)
    def mine(self, request):
        qs_mine = self.queryset.filter(assigned_to=request.user).filter(done=False)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_mine)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=False)
    def published(self, request):
        qs_published = self.queryset.filter(published=True).filter(done=False)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_published)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True, url_path='tag/(?P<tagid>[^/.]+)')
    def tag(self, request, pk=None, tagid=None):
        workitem: Workitem = object_or_not_found(Workitem, pk)
        tag: Tag = object_or_not_found(Tag, tagid)
        if request.method == 'POST':
            workitem.tag_add(tag)
        elif request.method == 'DELETE':
            workitem.tag_remove(tag)

        return Response(status=status.HTTP_204_NO_CONTENT)
        
    @action(methods=['post', 'delete'], detail=True, url_path='assign/(?P<userid>[^/.]+)')
    def assign(self, request, pk=None, userid=None):
        workitem: Workitem = object_or_not_found(Workitem, pk)
        user: User = object_or_not_found(User, userid)
        if request.method == 'POST':
            workitem.assignee_add(user)
        elif request.method == 'DELETE':
            workitem.assignee_remove(user)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def publish(self, request, pk=None):
        workitem: Workitem = object_or_not_found(Workitem, pk)
        if request.method == 'POST':
            workitem.published = True
        elif request.method == 'DELETE':
            workitem.published = False

        workitem.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkitemAssignmentViewSet(viewsets.ModelViewSet):
    """

    unverified:
    Load a list of workitems assignments that have not been verified
    """
    queryset = WorkitemAssignment.objects.all()
    serializer_class = WorkitemAssignmentSerializer
    renderer_classes = (WorkitemAssignmentJSONRenderer, )
    permission_classes = (IsAuthenticated, )

    @action(methods=['post', 'delete'], detail=True)
    def verify(self, request, pk=None):
        wa: WorkitemAssignment = object_or_not_found(WorkitemAssignment, pk)
        if request.method == 'POST':
            wa.verify()
        elif request.method == 'DELETE':
            wa.remove_verify()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def markdone(self, request, pk=None):
        wa: WorkitemAssignment = object_or_not_found(WorkitemAssignment, pk)
        if request.method == 'POST':
            wa.markdone()
        elif request.method == 'DELETE':
            wa.remove_markdone()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def unverified(self, request):
        qs_unverified = self.queryset.filter(verified=False)
        serializer_context = {'request': request}
        page = self.paginate_queryset(qs_unverified)
        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )
        return self.get_paginated_response(serializer.data)
