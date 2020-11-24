from django.shortcuts import render

# Importing database models:
from .models import ExternalDatabase

# Main index/home page:
def main_index(request):
    """
    The main index method is used to render the main html template for the django
    project that summarizes the status of all the connected external databases.

    The main purpose of this view is to query the django database for all instances
    of the ‘ExternalDatabase’ model. It then passes this QuerySet to the django html
    template. The reason this view function is so bare-bones is because most of the
    summary information that is to be displayed on the main_index.html page is related
    to the ‘ExternalDatabase’ model and is dynamically rendered by the template.

    This means that most of the logic for the main index page of the site is stored
    and performed in the actual django template itself.

    Args:
        request (http request): The http request that is sent to the server from
            the client.
    Returns:
        django.shortcuts.render: The django template rendered as html with full
            context.
            
    """
    # Querying database for all instances of ExternalDatabase objects:
    all_external_databases = ExternalDatabase.objects.all()

    # Building context to pass to template:
    context = {
    'external_databases' : all_external_databases
    }

    return render(request, "dashboard_core/main_index.html", context=context)
