from django import forms

from lostandfoundweb.models import Newuser
from lostandfoundweb.models import Storefound
from lostandfoundweb.models import Storelost
from lostandfoundweb.models import Storeclaim
from lostandfoundweb.models import Storematching
class NewuserForm(forms.ModelForm):
    class Meta:
        model=Newuser
        fields="__all__"

class StorelostForm(forms.ModelForm):
    class Meta:
        model=Storelost
        fields="__all__"

class StorefoundForm(forms.ModelForm):
    class Meta:
        model=Storefound
        fields="__all__"

class StoreclaimForm(forms.ModelForm):
    class Meta:
        model=Storeclaim
        fields="__all__"

class Storematching(forms.ModelForm):
    class Meta:
        model=Storematching
        fields="__all__"