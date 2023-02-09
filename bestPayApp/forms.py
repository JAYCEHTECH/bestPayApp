from django import forms
from django.contrib.auth.forms import UserCreationForm
from bestPayApp.models import CustomUser


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100'}))
    phone = forms.CharField(widget=forms.NumberInput(attrs={'class': 'input100 phone-num'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'email', 'phone', 'password1', 'password2']


class SendMessageForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Message'}))


class AirtimeForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input phone_input'}))
    amount = forms.FloatField(max_value=500, min_value=1, step_size=0.5,
                              widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    provider = forms.ChoiceField(choices=[(1, 'MTN'), (2, 'AirtelTigo'), (3, 'Vodafone'), (4, 'Glo')],
                                 widget=forms.Select(attrs={'class': 'form-control airtime-input'}))

    def clean(self):
        cleaned_data = super(AirtimeForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        amount = cleaned_data.get('amount')
        if not phone_number and not amount:
            raise forms.ValidationError('Fill all the spaces provided!')
        if not phone_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        if not amount:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone_number:
            if str(phone_number)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone_number)) != 12:
                raise forms.ValidationError(
                    'Check your number and try again. You may want to exclude the "0" after 233')


class VodafoneBundleForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    offers = forms.ChoiceField(choices=[(0.5, '0.50p (25MB)'), (1, 'GH₵1 (55MB)'), (2, 'GH₵2 (130MB)'),
                                        (5, 'GH₵5 (655MB)'), (10, 'GH₵10 (1.2GB)'), (20, 'GH₵20 (2.2GB)'),
                                        (50, 'GH₵50 (5.5GB)'), (100, 'GH₵100 (12GB)'), (200, 'GH₵200 (40GB)'),
                                        (300, 'GH₵300 (125GB)'), (400, 'GH₵400 (225GB)')],
                               widget=forms.Select(attrs={'class': 'form-control airtime-input'}))


class MTNBundleForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    offers = forms.ChoiceField(choices=[(0.5, '0.50p (24.05MB)'), (1, 'GH₵1 (48.10MB)'), (3, 'GH₵3 (471.70MB)'),
                                        (10, 'GH₵10 (971.82MB)'), (20, 'GH₵20 (1.61GB)'), (40, 'GH₵40 (3.23GB)'),
                                        (60, 'GH₵60 (4.84GB)'), (80, 'GH₵80 (6.45GB)'), (100, 'GH₵100 (10.64GB)'),
                                        (120, 'GH₵120 (12.77GB)'), (150, 'GH₵150 (15.96GB)'),
                                        (200, 'GH₵200 (35.84)'), (250, 'GH₵250 (44.80GB)'), (299, 'GH₵299 (53.58GB)')],
                               widget=forms.Select(attrs={'class': 'form-control airtime-input'}))

    def clean(self):
        cleaned_data = super(MTNBundleForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone_number:
            if str(phone_number)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone_number)) != 12:
                raise forms.ValidationError(
                    'Check your number and try again. You may want to exclude the "0" after 233')


class OtherMTNBundleForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    offers = forms.ChoiceField(choices=[('1.09', 'Kokrokoo 400MB, 20Min'), ('1', 'Video 183.49MB'), ('5', 'Video 917.43MB'),
                                        ('10', 'Video 1.79GB'), ('1s', 'Social Media 96.15MB'), ('5s', 'Social Media 480.77MB'),
                                        ('10s', 'Social Media 961.54MB')],
                               widget=forms.Select(attrs={'class': 'form-control airtime-input'}))

    def clean(self):
        cleaned_data = super(OtherMTNBundleForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone_number:
            if str(phone_number)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone_number)) != 12:
                raise forms.ValidationError(
                    'Check your number and try again. You may want to exclude the "0" after 233')


class AirtelTigoBundleForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    offers = forms.ChoiceField(choices=[(1, 'GH₵1 (55MB)'), (2, 'GH₵2 (130MB)'), (5, 'GH₵5 (655MB)'),
                                        (10, 'GH₵10 (1.2GB)'), (20, 'GH₵20 (2.2GB)'),
                                        (50, 'GH₵50 (5.6GB)'), (100, 'GH₵100 (12.3GB)'), (300, 'GH₵300 (128GB)'),
                                        (350, 'GH₵350 (150GB)'), (400, 'GH₵400 (230GB)')],
                               widget=forms.Select(attrs={'class': 'form-control airtime-input'}))

    def clean(self):
        cleaned_data = super(AirtelTigoBundleForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone_number:
            if str(phone_number)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone_number)) != 12:
                raise forms.ValidationError(
                    'Check your number and try again. You may want to exclude the "0" after 233')


class IShareBundleForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    offers = forms.ChoiceField(choices=[(2, 'GH₵2 (500MB)'), (4, 'GH₵4 (1.0GB)'), (7, 'GH₵7 (2.0GB)'),
                                        (10, 'GH₵10 (3.0GB)'), (12, 'GH₵12 (4.0GB)'), (15, 'GH₵15 (5.0GB)'),
                                        (18, 'GH₵18 (6.0GB)'), (22, 'GH₵22 (7.0GB)'), (25, 'GH₵25 (8.0GB)'),
                                        (30, 'GH₵30 (10GB)'), (45, 'GH₵45 (15GB)'), (60, 'GH₵60 (20GB)'),
                                        (75, 'GH₵75 (25GB)'), (90, 'GH₵90 (30GB)'), (120, 'GH₵120 (40GB)'),
                                        (150, 'GH₵150 (50GB)'), (285, 'GH₵285 (100GB)'), (560, 'GH₵560 (200GB)')],
                               widget=forms.Select(attrs={'class': 'form-control airtime-input'}))

    def clean(self):
        cleaned_data = super(IShareBundleForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone_number:
            if str(phone_number)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone_number)) != 12:
                raise forms.ValidationError(
                    'Check your number and try again. You may want to exclude the "0" after 233')


class SikaKokooBundleForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    offers = forms.ChoiceField(choices=[(3, 'GH₵3 (Sika Kokoo 500MB - 1day)'), (5, 'GH₵5 (Sika Kokoo 900MB - 3days)'),
                                        (6, 'GH₵6 (Sika Kokoo 1.2GB - 2days)'), (10, 'GH₵10 (Sika Kokoo 1.4GB - 5days)'),
                                        (11, 'GH₵11 (Sika Kokoo 2GB - 2days)'), (15, 'GH₵15 (Sika Kokoo 2.6GB - 4days)'),
                                        (20, 'GH₵20 (Sika Kokoo 3GB - 5days)'),(50, 'GH₵50 (Sika Kokoo 6.8GB - 15days)')],
                               widget=forms.Select(attrs={'class': 'form-control airtime-input'}))

    def clean(self):
        cleaned_data = super(SikaKokooBundleForm, self).clean()
        phone_number = cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        if phone_number:
            if str(phone_number)[:3] != "233":
                raise forms.ValidationError('Number must start with country code: Eg. 233XXXXXXXXX')
            if len(str(phone_number)) != 12:
                raise forms.ValidationError(
                    'Check your number and try again. You may want to exclude the "0" after 233')


class TvForm(forms.Form):
    account_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    amount = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input'}))
    provider = forms.ChoiceField(choices=[("DSTV", "DSTV"), ("GOTV", "GoTv"), ("STARTIMES", "StarTimesTv")],
                                 widget=forms.Select(attrs={'class': 'form-control airtime-input'}))

    def clean(self):
        cleaned_data = super(TvForm, self).clean()
        account_number = cleaned_data.get('phone_number')
        if not account_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        amount = cleaned_data.get('amount')
        if not account_number and not amount:
            raise forms.ValidationError('Fill all the spaces provided!')
        if not account_number:
            raise forms.ValidationError('Fill all the spaces provided!')
        if not amount:
            raise forms.ValidationError('Fill all the spaces provided!')


class TVCheckForm(forms.Form):
    account_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control airtime-input account-input'}))
    provider = forms.ChoiceField(choices=[("DSTV", "DSTV"), ("GOTV", "GoTv"), ("STARTIMES", "StarTimesTv")],
                                 widget=forms.Select(attrs={'class': 'form-control airtime-input provider-input'}))

    def clean(self):
        cleaned_data = super(TVCheckForm, self).clean()
        account_number = cleaned_data.get('account_number')
        if not account_number:
            raise forms.ValidationError('Fill all the spaces provided!')
