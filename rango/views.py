from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

def index(request):
    #Query the database for a list of ALL categories currently stored.
    #Order the categories by the number of likes in decending order.
    #Retreive the top 5 only - or all if less than 5.
    #Place the list in our context_dict dictionary (with out boldmessage)
    #that will be passed to the template engine

    #query the category model to retreive the top 5 categories
    #after query, we pass a reference to the list stored as variable
    #category_list to the dictionary context_dictionary
    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    #context_dict contains two key-value pairs
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    #render the response and send it back
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    #create a context dictionary which we can pass to 
    #the template rendering engine
    context_dict = {}

   # if the category slug is found in the Category model we can pull the associated pages
   #and add this to the context_dict
    try:
        #can we find a category name slug with the given name.
        #if we can't, the .get() method raises a DoesNotExist exception.
        #the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        #retreive all of the associated pages.
        #the filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        #adds our results list to the template context under name pages
        context_dict['pages'] = pages

        #we also add the category object from the database to the context dictionary
        #we'll use this in the template to verify that the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        # if we did not find the specified category we don't do anything - the template displays the 
        # "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    #go render the response and return it to the client
    return render(request, 'rango/category.html', context=context_dict)
