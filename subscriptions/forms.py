from django import forms
from django.core.mail import EmailMessage
# from .models import Diary
from .models import Subscription

class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前',max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル',max_length=30)
    message = forms.CharField(label='メッセージ',widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['name'].widget.attrs['class']='form-control col-9'
        self.fields['name'].widget.attrs['placeholder']="お名前をここに入力してください"
        self.fields['email'].widget.attrs['class']='form-control col-11'
        self.fields['email'].widget.attrs['placeholder']="メールアドレスをここに入力してください"
        self.fields['title'].widget.attrs['class']='form-control col-11'
        self.fields['title'].widget.attrs['placeholder']="タイトルをここに入力してください"
        self.fields['message'].widget.attrs['class']='form-control col-12'
        self.fields['message'].widget.attrs['placeholder']="メッセージをここに入力してください"

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name,email,message)
        from_email = 'admin@example.com'
        to_list = ['test@example.com']
        cc_list = [email]

        message = EmailMessage(subject=subject, body=message,from_email=from_email, to=to_list,cc=cc_list)
        message.send()


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = (
            'service', 'custom_name', 'price', 'currency',
            'start_date', 'interval_value', 'interval_unit', 'memo'
        )
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'interval_value': forms.NumberInput(attrs={'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

        self.fields['interval_unit'].empty_label = None
        self.fields['interval_unit'].initial = 'month'

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get("service")
        custom_name = cleaned_data.get("custom_name")

        if not service:
            self.add_error("service", "サービスを選択してください")

        if service and service.category.group == "other" and not custom_name:
            self.add_error("custom_name", "その他の場合はサービス名を入力してください")

        return cleaned_data
    
    def clean_interval_value(self):
        value = self.cleaned_data.get('interval_value')

        if value is not None and value < 1:
            raise forms.ValidationError("1以上の数値を入力してください")

        return value

