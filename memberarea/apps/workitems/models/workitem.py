from datetime import datetime

from django.conf import settings
from django.db import models

from memberarea.apps.authentication.models import User
from memberarea.apps.core.models import TimestampedModel
from memberarea.apps.tags.models import Tag
from ..exceptions import (
    AlreadyAssigned, MaxAssigneesReached
)


class Workitem(TimestampedModel):
    title = models.CharField(max_length=80)
    description = models.TextField()
    published = models.BooleanField(db_index=True, default=False)
    duration_expected = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_workitems')
    due_at = models.DateField(db_index=True)
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='WorkitemAssignment',
        through_fields=('workitem', 'assignee')
    )
    max_assignees = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    done = models.BooleanField(default=False)

    def assignee_add(self, assignee: User):
        if assignee is None:
            return
        if assignee in self.assigned_to.all():
            raise AlreadyAssigned()
        if self.assigned_to.count() >= self.max_assignees:
            raise MaxAssigneesReached()

        wa = WorkitemAssignment(workitem=self, assignee=assignee)
        wa.save()

    def assignee_remove(self, assignee: User):
        if assignee is None:
            return
        if assignee in self.assigned_to.all():
            wa = WorkitemAssignment.objects.get(workitem=self, assignee=assignee)
            wa.delete()

    def tag_add(self, tag: Tag):
        if tag is None:
            return
        if tag not in self.tags.all():
            self.tags.add(tag)

    def tag_remove(self, tag: Tag):
        if tag is None:
            return
        if tag in self.tags.all():
            self.tags.remove(tag)

    @property
    def all_done(self) -> bool:
        for wa in self.assigned_to.all():
            if wa.done is None:
                return False
        return True

    def has_object_tag_permission(self, request):
        return request.user.has_perm('tag_workitem') or request.user == self.created_by

    class Meta:
        ordering = ('-due_at', )
        permissions = (
            ('assign_workitem', 'Can assign a workitem to an user'),
            ('tag_workitem', 'Can assign a tag to a workitem'),
        )


class WorkitemAssignment(TimestampedModel):
    workitem = models.ForeignKey(Workitem, on_delete=models.CASCADE, related_name='assignments')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assigned_workitems')
    duration_real = models.IntegerField(null=True, blank=True)
    done = models.BooleanField(db_index=True, default=False)
    done_at = models.DateField(null=True, blank=True)
    verified = models.BooleanField(db_index=True, default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='verified_workitems',
        null=True,
        blank=True
    )

    def verify(self, user: User) -> bool:
        if user is None:
            return False
        self.verified = True
        self.verified_by = user
        self.verified_at = datetime.now()
        self.save()
        return True

    def remove_verify(self) -> bool:
        self.verified = False
        self.verified_by = None
        self.verified_at = None
        self.save()
        return True

    def markdone(self):
        self.done = True
        self.done_at = datetime.now()
        self.save()
        if self.workitem.all_done:
            self.workitem.done = True
            self.workitem.save()

    def remove_markdone(self):
        self.workitem.done = False
        self.workitem.save()
        self.done = True
        self.done_at = datetime.now()
        self.save()

    @staticmethod
    def has_verify_permission(request):
        return request.user.has_perm('verify_workitemassignment')

    def has_object_markdone_permission(self, request):
        return request.user.has_perm('markdone_workitemassignment') or request.user == self.assignee

    class Meta:
        permissions = (
            ('verify_workitemassignment', 'Can verify a workitem assignment'),
            ('markdone_workitemassignment', 'Can mark a workitem assignment as done'),
        )

