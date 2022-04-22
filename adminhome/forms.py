from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import ParkingSpot, ParkingCategory, Booking, Vehicle
from django.contrib.auth.models import User

class CustomUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        # field_classes = {"username": UsernameField}


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class HomeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(HomeForm, self).__init__(*args, **kwargs)

        self.fields["about_header"] = forms.CharField(label='About Us Header', initial=extra["about"]["about_header"],
                                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields["about_body"] = forms.CharField(label='About Us Body', initial=extra["about"]["about_body"],
                                                    widget=forms.Textarea(attrs={'class': 'form-control'}))

        self.fields["ameneties_header"] = forms.CharField(label='Ameneties Header',
                                                          initial=extra["ameneties"]["ameneties_header"],
                                                          widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields["ameneties_body"] = forms.CharField(label='Ameneties Body',
                                                        initial=extra["ameneties"]["ameneties_body"],
                                                        widget=forms.Textarea(attrs={'class': 'form-control'}))

        self.fields["phone"] = forms.CharField(label='Phone', initial=extra["contact"]["phone"],
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields["email"] = forms.CharField(label='Email', initial=extra["contact"]["email"],
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
        self.fields["location"] = forms.CharField(label='Location', initial=extra["contact"]["location"],
                                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

        for i, c in enumerate(extra["carousel"]):
            self.fields['carousel_header_%s' % i] = forms.CharField(label=('Carousel %s Header: ' % (i + 1)),
                                                                    initial=c["header"], widget=forms.TextInput(
                    attrs={'class': 'form-control'}))
            self.fields['carousel_body_%s' % i] = forms.CharField(label=('Carousel %s Contents: ' % (i + 1)),
                                                                  initial=c["body"], widget=forms.Textarea(
                    attrs={'class': 'form-control'}))
            self.fields['carousel_image_%s' % i] = forms.ImageField(label=('Carousel %s Image: ' % (i + 1)),
                                                                    required=False)


class ParkingCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParkingCategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ParkingCategory
        fields = "__all__"


class ParkingSpotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParkingSpotForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ParkingSpot
        fields = "__all__"


class DatePickerInput(forms.DateInput):
        input_type = 'date'

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput)
    end_date = forms.DateField(widget=DatePickerInput)

class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = "__all__"

class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Vehicle
        fields = ['name', 'model', 'make', 'build', 'color', 'insurance_doc']


class VerifyVehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VerifyVehicleForm, self).__init__(*args, **kwargs)
        self.fields['insurance_expiry_date'] = forms.DateTimeField(help_text="Format yyyy-mm-dd")

    class Meta:
        model = Vehicle
        fields = ['insurance_expiry_date']
