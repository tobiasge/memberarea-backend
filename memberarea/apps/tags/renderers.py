from memberarea.apps.core.renderers import MemberareaJSONRenderer


class TagJSONRenderer(MemberareaJSONRenderer):
    object_label = 'tag'
    pagination_object_label = 'tags'
    pagination_count_label = 'tagsCount'
