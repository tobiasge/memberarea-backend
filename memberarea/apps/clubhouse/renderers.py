from memberarea.apps.core.renderers import MemberareaJSONRenderer


class ClubhouseJSONRenderer(MemberareaJSONRenderer):
    object_label = 'clubhouse'
    pagination_object_label = 'clubhouses'
    pagination_count_label = 'clubhouseCount'


class RoomJSONRenderer(MemberareaJSONRenderer):
    object_label = 'room'
    pagination_object_label = 'rooms'
    pagination_count_label = 'roomCount'


class DefectJSONRenderer(MemberareaJSONRenderer):
    object_label = 'defect'
    pagination_object_label = 'defects'
    pagination_count_label = 'defectCount'
