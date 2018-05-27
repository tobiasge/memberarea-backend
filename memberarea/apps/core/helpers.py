from rest_framework.exceptions import NotFound


def object_or_not_found(tofind, pk):
    try:
        result = tofind.objects.get(pk=pk)
    except tofind.DoesNotExist:
        raise NotFound('A {} with this id does not exist.'.format(tofind.__name__).lower())
    return result
