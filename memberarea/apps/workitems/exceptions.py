from rest_framework.exceptions import APIException

class AlreadyAssigned(APIException):
    status_code = 400
    default_detail = 'Workitem is alredy assigned to this user'
    default_code = 'workitem_already_assigned'

class MaxAssigneesReached(APIException):
    status_code = 400
    default_detail = 'The maximum assignee number is reached'
    default_code = 'workitem_max_assignment_reached'
