
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


# csrf token

``` 
# Cross-Site Request Forgery in AJAX requests

You have learned *Cross-Site Request Forgery* in [Chapter 2](c61ca611-9b95-4014-8e4d-8a00c6b70a7b.xhtml), *Enhancing Your Blog with Advanced Features*. With the CSRF protection active, Django checks for a CSRF token in all POST requests. When you submit forms, you can use the {% csrf_token %} template tag to send the token along with the form. However, it is a bit inconvenient for AJAX requests to pass the CSRF token as a POST data in with every POSTrequest. Therefore, Django allows you to set a custom X-CSRFToken header in your AJAX requests with the value of the CSRF token. This allows you to set up jQuery or any other JavaScript library to automatically set the X-CSRFToken header in every request.

In order to include the token in all requests, you need to take the following steps:

1. Retrieve the CSRF token from the csrftoken cookie, which is set if CSRF protection is active
2. Send the token in the AJAX request using the X-CSRFToken header

You can find more information about CSRF protection and AJAX at <https://docs.djangoproject.com/en/2.0/ref/csrf/#ajax>.

Edit the last code you included in your base.html template and make it look like the following:

```
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>
<script>
  var csrftoken = Cookies.get('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $(document).ready(function(){
    {% block domready %}
    {% endblock %}
  });
</script>
```

The preceding code is as follows:

1. We load the JS Cookie plugin from a public CDN so that we can easily interact with cookies. JS Cookie is a lightweight JavaScript for handling cookies. You can learn more about it at <https://github.com/js-cookie/js-cookie>.
2. We read the value of the csrftoken cookie with Cookies.get().

1. We define the csrfSafeMethod() function to check whether an HTTP method is safe. Safe methods don't require CSRF protection—these are GET, HEAD, OPTIONS, and TRACE.
2. We set up jQuery AJAX requests using $.ajaxSetup(). Before each AJAX request is performed, we check whether the request method is safe and the current request is not cross-domain. If the request is unsafe, we set the X-CSRFToken header with the value obtained from the cookie. This setup will apply to all AJAX requests performed with jQuery.

The CSRF token will be included in all AJAX requests that use unsafe HTTP methods, such as POST or PUT.
```

## with 

Edit the images/image/detail.html template of the images application, and consider the following line:

```
{% with total_likes=image.users_like.count %}
```

Replace the preceding one with the following one:

```
{% with total_likes=image.users_like.count users_like=image.users_like.all %}
```

Then, modify the <div> element with the image-info class, as follows:

```
<div class="image-info">
  <div>
    <span class="count">
      <span class="total">{{ total_likes }}</span>
      like{{ total_likes|pluralize }}
    </span>
    <a href="#" data-id="{{ image.id }}" data-action="{% if  
    request.user in users_like %}un{% endif %}like" 
    class="like button">
      {% if request.user not in users_like %}
        Like
      {% else %}
        Unlike
      {% endif %}
    </a>
  </div>
  {{ image.description|linebreaks }}
</div>
```


## 自定义装饰器

We will restrict our AJAX views to allow only requests generated via AJAX. The Django request object provides an is_ajax() method that checks whether the request is being made with XMLHttpRequest, which means it is an AJAX request. This value is set in the HTTP_X_REQUESTED_WITH HTTP header, which is included in AJAX requests by most JavaScript libraries.

We will create a decorator for checking the HTTP_X_REQUESTED_WITH header in our views. A decorator is a function that takes another function and extends the behavior of the latter without explicitly modifying it. If the concept of decorators is foreign to you, you might like to take a look at <https://www.python.org/dev/peps/pep-0318/> before you continue reading.

Since our decorator will be generic and could be applied to any view, we will create a common Python package in our project. Create the following directory and files inside the bookmarks project directory:

```
common/
    __init__.py
    decorators.py
```

Edit the decorators.py file and add the following code to it:

```
from django.http import HttpResponseBadRequest

def ajax_required(f):
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
```

The preceding code is our custom ajax_required decorator. It defines a wrap function that returns an HttpResponseBadRequest object (HTTP 400 code) if the request is not AJAX. Otherwise, it returns the decorated function.

Now, you can edit the views.py file of the images application and add this decorator to your image_like AJAX view, as follows:

```
from common.decorators import ajax_required

@ajax_required
@login_required
@require_POST
def image_like(request):
    # ...
```

If you try to access http://127.0.0.1:8000/images/like/ directly with your browser, you will get an HTTP 400 response.
