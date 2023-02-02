from django.db import models
from django.template.defaultfilters import slugify
#slugify replaces whitespace with hyphens 

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

