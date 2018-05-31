from memberarea.apps.core.renderers import MemberareaJSONRenderer


class WorkitemJSONRenderer(MemberareaJSONRenderer):
    object_label = 'workitem'
    pagination_object_label = 'workitems'
    pagination_count_label = 'workitemCount'


class WorkitemAssignmentJSONRenderer(MemberareaJSONRenderer):
    object_label = 'workitemAssignment'
    pagination_object_label = 'workitemAssignments'
    pagination_count_label = 'workitemAssignmenCount'


class WorkedHoursStatsJSONRenderer(MemberareaJSONRenderer):
    object_label = 'workedHoursStat'
    pagination_object_label = 'workedHoursStats'
    pagination_count_label = 'WorkedHoursStatsCount'
