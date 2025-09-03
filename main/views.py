from django.shortcuts import render

# Create your views here.

def show_main(request):
    context = {
        'npm' : '2406413981',
        'name': 'Justin Timothy Wirawan Super Sigma Ayanongkoji',
        'class': 'PBP D'
    }

    return render(request, "main.html", context)