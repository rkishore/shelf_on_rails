# Create your views here.
from django.http import HttpResponse
import datetime
from django.shortcuts import render_to_response
from django import forms

class Wishlist(forms.Form):
    
    
    STORE_CHOICES = (
                     ('jcrew', 'JCREW'),
                     ('express', 'EXPRESS'),
                     )
    SEX_CHOICES = (
                   (0, 'MALE'),
                   (1, 'FEMALE'),
                   (2, 'ALL'),
                   )
    
    ITEM_CATEGORY_CHOICES = (
                             (0, 'SHIRTS'),
                             (1, 'PANTS'),
                             (2, 'SWEATERS'),
                             (3, 'JEANS'),
                             (4, 'OUTERWEAR'),
                             (5, 'UNDERWEAR'),
                             (7, 'EVERYTHING')
                             )
    
    #store = forms.CharField(max_length=100, choices = STORE_CHOICES)
    store = forms.ChoiceField(choices = STORE_CHOICES)
    item_category = forms.ChoiceField(choices = ITEM_CATEGORY_CHOICES)
    sex_category = forms.ChoiceField(choices = SEX_CHOICES)
    size = forms.IntegerField()
    color = forms.IntegerField()
    howmany = forms.IntegerField()

    ''' QUESTION 
    1. A user must be able to select multiple items of different category from the same store
    2. A user must be able to choose items from different stores.
    
    '''

    
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def wishlist(request):
    if request.method == 'POST': # If the form has been submitted...
        form = Wishlist(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            store = form.cleaned_data['store']
            item_category = form.cleaned_data['item_category']
            sex_category = form.cleaned_data['sex_category']
            size = form.cleaned_data['size']
            color = form.cleaned_data['color']
            howmany = form.cleaned_data['howmany']
            
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = Wishlist() # An unbound form
    print form
    
    return render_to_response('wishlist.html', {
        'form': form,
    })