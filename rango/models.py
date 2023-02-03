from django.db import models
from django.template.defaultfilters import slugify
#slugify replaces whitespace with hyphens 
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    # slugify() makes the slugs lower case so if we have two categories with one
    #called Django and another called django we can't determine which corresponds to the slug.
    #we add unique = True to eliminate this.
    slug = models.SlugField(unique=True)

    #the slug field is set using output of the slugify() function as the new fields value.
    # once set, the overriden save() calls the parent save() method defined in the base 
    # django.db.models.Model class which performs the necessary logic to process your changes 
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH =128
    URL_MAX_LENGTH = 200
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    #this line is required. Links UserProfile to a User model instance.
    #notice we reference the User model using a one-to-one relationship.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #the additional attributes we wish to include.
    #we set blank=True for both fields, users don't need to supply a value.
    #ImageField has an upload_to attribute. The value of this attribute is conjoined with the project's
    #MEDIA_ROOT setting to provide a path with which uploaded profile images will be stored.
    #e.g. a MEDIA_ROOT of <workspace>/tango_with_django_project/media/ and upload_to attribute of 
    #profile_images results in all profile images being stored in the directory:
    #<workspace>/tango_with_django_project/media/profile_images/.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    #use the __str__ method to return a meaningful value 
    def __str__(self):
        return self.user.username