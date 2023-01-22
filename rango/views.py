from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #notes from  twr2 page 57 on pdf
    #construct a dictionary to pass to the template engine as its context.
    #note that teh key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    #return a rendered response to send to the client.
    #we make use of the shortcut function to make our lives easier.
    #note that the first parameter is the template we wish to use.
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")
