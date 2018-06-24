
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
