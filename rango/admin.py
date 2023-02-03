from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
#Add in classes to customise the page and category admin interfaces

#adds title,category and url as columns in the pages admin view
class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'url')

#the slug field automatically populates whenyou type into the name field.
#we avoid having to rely on users to type fill it out with hyphens replacing the
#spaces 
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)