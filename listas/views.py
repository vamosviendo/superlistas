from django.http import HttpResponse


def home_page(request):
    return HttpResponse('<html><title>Listas de tareas</title></html>')
