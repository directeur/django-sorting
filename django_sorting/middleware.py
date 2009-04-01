class SortingMiddleware(object):
    """
    Inserts a variable representing the field (with direction of sorting)
    onto the request object if it exists in either **GET** or **POST** 
    portions of the request.
    """
    def process_request(self, request):
        try:
            request.field = str(request.REQUEST['sort'])
        except (KeyError, ValueError, TypeError):
            request.field = ''

        try:
            direction = str(request.REQUEST['dir'])
        except (KeyError, ValueError, TypeError):
            direction = 'desc'

        if direction == 'asc' and request.field:
            request.field = '-'+request.field

