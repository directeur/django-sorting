def get_field(self):
    try:
        field = request.REQUEST['sort']
    except (KeyError, ValueError, TypeError):
        field = ''
    return (self.direction == 'desc' and '-') + field

def get_direction(self):
    try:
        return request.REQUEST['dir']
    except (KeyError, ValueError, TypeError):
        return 'desc'

class SortingMiddleware(object):
    """
    Inserts a variable representing the field (with direction of sorting)
    onto the request object if it exists in either **GET** or **POST** 
    portions of the request.
    """
    def process_request(self, request):
        request.__class__.field = property(get_field)
        request.__class__.direction = property(get_direction)