from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    #The user won't be able to enter a value for the hidden fields
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #we say the slug field isn't required by the form. Our model is responsible for populating this field when the form is saved
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    #An inline class to provide additional information on the form.
    class Meta:
        #Provide an association between the ModelForm and a model
        #enables django to take care of creating a form in the image of the specified model. Also helps with error flagging and saving
        #and displaying data in the form.
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    #Even though we have hidden fields, we still need to include that field in the form. E.g. if in fields we excluded views, 
    #the form would not contain that field despite it being specified and the form wouldn't return the value 0 for that field, 
    #potentially yielding an error if the model wasn't set up so that these fields had default = 0. 
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #Note that the max_length parameters we supply to each field are idnetical to those we specifed
    #in the data models

    class Meta:
        #Providean association between the ModelForm and a model
        model = Page

        #What fields do we want to include in our form?
        #This way we don't need every field in the model present.
        #Some fields may allow NULL values; we may not want to include them.
        #Here, we are hiding the foreign key.
        #we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (don't include the category field).
        #fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    #meta classes describe additional properties about the particular class to which it belongs.
    class Meta:
        model = User
        #we want to show the username, email and password fields associated with the User model.
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        #for the user field within the UserProfile model, we need to make the association when we register
        #the user. When we create a UserProfile instance, we won't yet have the User instance to refer to.
        fields = ('website', 'picture',)