from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import ParkingSpot, ParkingCategory

class CustomUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class':'form-control'})

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class':'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})

class HomeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(HomeForm, self).__init__(*args, **kwargs)

        self.fields["about_header"] = forms.CharField(label='About Us Header', initial=extra["about"]["about_header"], widget= forms.TextInput(attrs={'class':'form-control'}))
        self.fields["about_body"] = forms.CharField(label='About Us Body', initial=extra["about"]["about_body"], widget= forms.Textarea(attrs={'class':'form-control'}))
        
        self.fields["ameneties_header"] = forms.CharField(label='Ameneties Header', initial=extra["ameneties"]["ameneties_header"], widget= forms.TextInput(attrs={'class':'form-control'}))
        self.fields["ameneties_body"] = forms.CharField(label='Ameneties Body', initial=extra["ameneties"]["ameneties_body"], widget= forms.Textarea(attrs={'class':'form-control'}))
        
        self.fields["phone"] = forms.CharField(label='Phone', initial=extra["contact"]["phone"], widget= forms.TextInput(attrs={'class':'form-control'}))
        self.fields["email"] = forms.CharField(label='Email', initial=extra["contact"]["email"], widget= forms.TextInput(attrs={'class':'form-control'}))
        self.fields["location"] = forms.CharField(label='Location', initial=extra["contact"]["location"], widget= forms.TextInput(attrs={'class':'form-control'}))

        for i, c in enumerate(extra["carousel"]):
            self.fields['carousel_header_%s' % i] = forms.CharField(label=('Carousel %s Header: ' % (i+1)), initial=c["header"], widget= forms.TextInput(attrs={'class':'form-control'}))
            self.fields['carousel_body_%s' % i] = forms.CharField(label=('Carousel %s Contents: ' % (i+1)), initial=c["body"], widget= forms.Textarea(attrs={'class':'form-control'}))
            self.fields['carousel_image_%s' % i] = forms.ImageField(label=('Carousel %s Image: ' % (i+1)), required=False)

class ParkingCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParkingCategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ParkingCategory
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data['name']
        if ParkingCategory.objects.filter(name=name).exists():
            self._errors['name'] = self.error_class(['Parking Category already exists!'])
        return name


class ParkingSpotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParkingSpotForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ParkingSpot
        fields = "__all__"

    def clean(self):
        super(ParkingSpotForm, self).clean()

        name = self.cleaned_data.get('name')
        parking_category_id = self.cleaned_data.get('parking_category_id')

        if ParkingSpot.objects.filter(name=name).exists():
            parking_spot = ParkingSpot.objects.get(name=name)
            if parking_spot.parking_category_id == parking_category_id:
                self._errors['name'] = self.error_class([
                    'This Parking Spot already exists under the selected Parking Category'])

        return self.cleaned_data
