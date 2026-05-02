from django import forms
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import Subscription
import resend


class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control col-9',
            'placeholder': "お名前をここに入力してください"
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control col-11',
            'placeholder': "メールアドレスをここに入力してください"
        })
        self.fields['title'].widget.attrs.update({
            'class': 'form-control col-11',
            'placeholder': "タイトルをここに入力してください"
        })
        self.fields['message'].widget.attrs.update({
            'class': 'form-control col-12',
            'placeholder': "メッセージをここに入力してください"
        })

    def send_email(self):
        print("send_email 実行された")
        print("CONTACT_EMAIL:", settings.CONTACT_EMAIL)
        print("DEFAULT_FROM_EMAIL:", settings.DEFAULT_FROM_EMAIL)
        # APIキーセット
        resend.api_key = settings.RESEND_API_KEY

        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'title': self.cleaned_data['title'],
            'message': self.cleaned_data['message'],
        }

        subject = f"【お問い合わせ】{context['title']}"

        body = render_to_string(
            'inquiry/email/inquiry.txt',
            context
        )

        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": settings.CONTACT_EMAIL,
            "cc": context['email'],
            "subject": subject,
            "text": body,
        })

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