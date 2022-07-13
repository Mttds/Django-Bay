from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import AuctionListing, AuctionBid, AuctionComment

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'image_url', 'start_price', 'category']

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('title', css_class='form-control'),
        Field('description', css_class='form-control'),
        Field('image_url', css_class='form-control'),
        Field('start_price', css_class='form-control'),
        Field('category', css_class='form-control'),
    )

class BidForm(forms.ModelForm):
    class Meta:
        model = AuctionBid
        fields = ['price']

class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add bootstrap form-control class to each field
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    content = forms.CharField(widget=forms.Textarea)
