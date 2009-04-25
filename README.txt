How to use django-sorting
----------------------------

``django-sorting`` allows for easy sorting, and sorting links generation 
without modifying your views.

There are really 5 steps to setting it up with your projects.

1. List this application in the ``INSTALLED_APPS`` portion of your settings
   file.  Your settings file might look something like::
   
       INSTALLED_APPS = (
           # ...
           'django_sorting',
       )

2. Install the sorting middleware. Your settings file might look something
   like::
   
       MIDDLEWARE_CLASSES = (
           # ...
           'django_sorting.middleware.SortingMiddleware',
       )

3. If it's not already added in your setup, add the request context processor.
   Note that context processors are set by default implicitly, so to set them
   explicitly, you need to copy and paste this code into your under
   the value TEMPLATE_CONTEXT_PROCESSORS::
   
        ("django.core.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request")

4. Add this line at the top of your template to load the sorting tags:

       {% load sorting_tags %}


5. Decide on a variable that you would like to sort, and use the
   autosort tag on that variable before iterating over it.    
       
       {% autosort object_list %}
       
   
6. Now, you want to display different headers with links to sort 
your objects_list:
   
    <tr>
       <th>{% anchor first_name Name %}</th>
       <th>{% anchor creation_date Creation %}</th>
        ...
    </tr>

    The first argument is a field of the objects list, and the second 
    one(optional) is a title that would be displayed. The previous 
    snippet will be rendered like this:

    <tr>
        <th><a href="/path/to/your/view/?sort=first_name" title="Name">Name</a></th>
        <th><a href="/path/to/your/view/?sort=creation_date" title="Name">Creation</a></th>
        ...
    </tr>


That's it!  


