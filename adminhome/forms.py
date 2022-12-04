from datetime import datetime
import pytz

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import ParkingSpot, ParkingCategory, Booking, Vehicle, BillDetail, Payment, Poll
from .enums import PaymentMethod


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


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(user, *args, **kwargs)

    class Meta:
        model = User
        # fields = ['first_name', 'last_name', 'email', 'username']


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

class CheckAvailabilityDateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput)
    end_date = forms.DateField(widget=DatePickerInput)

    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        today_date = datetime.now(pytz.timezone('US/Central')).date()
        if start_date < today_date:
            raise forms.ValidationError("Start date should be greater than today's date {}.".format(today_date))
        if end_date <= start_date:
            raise forms.ValidationError("End date should be strictly greater than start date.")


class ShowSheduleDateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput)
    end_date = forms.DateField(widget=DatePickerInput)

    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if end_date <= start_date:
            raise forms.ValidationError("End date should be strictly greater than start date.")


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['parking_spot_id'].required = False
        self.fields['lease_doc_url'].required = False
        self.fields['admin_comments'].required = False

    class Meta:
        model = Booking
        fields = "__all__"

class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Vehicle
        fields = ['name', 'model', 'make', 'build', 'color', 'insurance_doc']


class VehicleChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VehicleChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Vehicle
        fields = ['name', 'model', 'make', 'build', 'color', 'insurance_doc']

class VerifyVehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VerifyVehicleForm, self).__init__(*args, **kwargs)
        self.fields['insurance_expiry_date'] = forms.DateTimeField(help_text="Format yyyy-mm-dd", widget=DatePickerInput)

    class Meta:
        model = Vehicle
        fields = ['insurance_expiry_date']


class BillDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BillDetailForm, self).__init__(*args, **kwargs)
        self.fields['init_meter_reading'] = forms.IntegerField(label='Initial Meter Reading', required=False, initial=0)
        self.fields['end_meter_reading'] = forms.IntegerField(label='End Meter Reading', required=False, initial=0)
        self.fields['paid_amount'] = forms.DecimalField(label='Paid Amount', initial=0)
        self.fields['unpaid_amount'] = forms.DecimalField(label='Unpaid Amount', initial=0)
        self.fields['misc_charges'] = forms.DecimalField(label='Miscellaneous Charges', required=False, initial=0)
        self.fields['comments'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)


    class Meta:
        model = BillDetail
        fields = ['init_meter_reading', 'end_meter_reading', 'paid_amount', 'unpaid_amount', 'misc_charges', 'comments']

class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['method'] = forms.ChoiceField(choices=PaymentMethod.choices)
        self.fields['amount'] = forms.DecimalField(label='Amount', initial=0)
        
    class Meta:
        model = Payment
        fields = ['method', 'amount']

#### CSCW: Begin ####
class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['option_one', 'option_two', 'option_three']
