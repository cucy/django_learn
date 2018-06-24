
# start

``` 
(sx3.5.3) ➜  django_learn git:(master) ✗ django-admin startproject bookmarks
(sx3.5.3) ➜  django_learn git:(master) ✗  cd bookmarks
(sx3.5.3) ➜  bookmarks git:(master) ✗ django-admin startapp account

```


## slug field

``` 
from django.utils.text import slugify

class Image(models.Model):
    # ...
    def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super(Image, self).save(*args, **kwargs)

```


# form

``` 

from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }
        
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url
```
