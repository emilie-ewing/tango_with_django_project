from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout

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

    #query the page model to get the 5 most viewed pages
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    #context_dict contains two key-value pairs (three after adding pages from chap 6 exercises)
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    

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

@login_required
def add_category(request):
    #create a category form
    form = CategoryForm()

    #A HTTP POST? Did the user submit data via the form
    if request.method == 'POST':
        #we handle the POST request through the same URL
        form = CategoryForm(request.POST)

        #Have we been provided with a valid form?
        if form.is_valid():
            #Save the new category to the database
            form.save(commit=True)
            #now that the category is saved, we could confirm this.
            #For now, just redirect the user back to tne index view
            return redirect(reverse('rango:index'))
            #return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            #the supplied form contains errors - just print them to the terminal
            print(form.errors)

    #handles the three scenarios:
    #- showing a new, blank form for adding a category
    #- saving form data provided by the user to the associated model, and redirecting the user to the Rango homepage, and
    #- if there are any errors, redisplay the form with error messages

    #will handle the bad form, new form or no form cases. Render the form with error messages (if any).
    #the add_category.html page is a template which contains the relevant Django template code and HTML for the form and page.
    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    #You cannot add a page to a Category that does not exist
    if category is None:
        return redirect(reverse('rango:index'))
        #return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                #redirect the user to show_category() view when page has been created
                #we use the redirect() and reverse() functions to redirect the user and lookup the appropriate URL
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
            else:
                print(form.errors)
        
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    # a boolean value for telling the template whether the registration was successful.
    #set to false initially, code changes value to True when registration succeeds.
    registered = False

    #if it's a HTTP POST, we're interested in processing the data 
    if request.method == 'POST':
        #attempt to grab information from the raw form information. Note that we make use of both UserForm and
        #UserProfileForm
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        #If the two forms are valid save the user's form data to the database
        if user_form.is_valid() and profile_form.is_valid():
            #save the users form data to the database.
            user = user_form.save()

            #hash the password with the set_password method. Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            #sort out the UserProfile instance. Since we need to set the user attribute ourselves, we set
            #commit=False. This delays saving the model until we are ready to avoid integrity problems.
            #the information from the UserProfile form is passed onto a new instance of the UserProfile model. The UserProfile
            #contains a foreign key reference to the standard Django User model but the UserProfile deosn't provide this information
            #so trying to save the new isntance in an incomplete state would raise a referential integrity error. 
            #we add the user reference on the line after and then use save() to manually save the new instance.
            profile = profile_form.save(commit=False)
            profile.user = user

            #if the user provided a profile picture, we need to get it from the input form and put it in 
            #the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #save the UserProfile model instance
            profile.save()

            #update our variable to indicate that the template registration was successful
            registered = True
        else:
            #invalid form or forms - mistakes or something else. Print problems to the terminal
            print(user_form.errors, profile_form.errors)
    else:
        #not an HTTP POST, so we render our form using two ModelForm instances. These forms will be
        #blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    #render the template depending on the context.
    return render(request, 'rango/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    #if the request is an HTTP POST, try to pull out the relevant information. We can handle processing the form
    if request.method == 'POST':
        #gather ther username and password provided by the user. This information is obtained from the login form.
        #we use request.POST.get('<variable>') as opposed to request.POST['<variable>'] because the 
        #request.POST.get('<variable>') returns None if the value does not exist, while request.POST['<variable>']
        #will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        #use Django's machinery to try to see if the username/password combination is valid - if it is, a User object 
        #is returned.
        user = authenticate(username=username, password=password)

        #if we have a user object, the details are correct
        #If None (Python's way of representing the absense of a value), no user with matching credentials were found
        if user:
            #is the account active? It could have been disabled
            if user.is_active:
                #if the account is valid and active, we can log the user in - we'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                #an inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            #bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    #The request is not an HTTP POST, so display the login form.
    #this scenario would most likely be a HTTP GET.
    else:
        #no context variables to pass to the template system, hence the blank directory object
        return render(request, 'rango/login.html')

@login_required 
def restricted(request):
    return render(request, 'rango/restricted.html')

#we use the login_required() decorator to ensure only those logged in can access the view
#the logout function ensures the session is ended.
@login_required
def user_logout(request):
    #since we know the user is logged in, we can now just log them out.
    logout(request)
    #Take the user back to the homepage
    return redirect(reverse('rango:index'))