from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html', {
        'texto_nuevo_item': request.POST.get('texto_item', '')
    })
