from django.shortcuts import render
from streams.forms import StreamForm

# Create your views here.


def stream_page(request):
    context = {
        'pagename': 'Стримец',
        'page_title': 'Стрим',
    }

    if request.method == 'POST':
        form = StreamForm(request.POST)
        if form.is_valid():
            stream_url(context, form, request)
        else:
            context['error'] = True
        context['form'] = form

    elif request.method == 'GET':
        context['form'] = StreamForm()
        context['has_data'] = False

    return render(request, 'stream_link.html', context)


def stream_url(context, form, request):
    a = form.data['first']
    b = form.data['second']
    context['has_data'] = True
    context['source'] = a
    for i in range(8):
        index = 24
        b = b[:index] + b[index + 1:]
        index += 1
    b = b.split('/')
    help_me = '/embed/'
    b = b[0]+'//'+b[2]+help_me+b[3]
    context['b'] = b
    return render(request, 'stream_link.html', context)
