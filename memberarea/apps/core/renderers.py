import json

from rest_framework.renderers import JSONRenderer


class MemberareaJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = None
    pagination_object_label = 'objects'
    pagination_count_label = 'count'
    pagination_next_label = 'next'
    pagination_previous_label = 'previous'

    def render(self, data, media_type=None, renderer_context=None):
        
        if data is None:
            return ''
        if data.get('results', None) is not None:
            return json.dumps({
                self.pagination_object_label: data['results'],
                self.pagination_count_label: data['count'],
                self.pagination_next_label: data['next'],
                self.pagination_previous_label: data['previous'],
            })

        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `error` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        elif data.get('error', None) is not None:
            error = data.get('error')
            # Prevent nested error fields
            if error.get('error', None) is not None:
                return super(MemberareaJSONRenderer, self).render(data.get('error'))
            return super(MemberareaJSONRenderer, self).render(data)
        else:
            if self.object_label is None:
                return json.dumps(
                    data
                )
    
            return json.dumps({
                self.object_label: data
            }) 
