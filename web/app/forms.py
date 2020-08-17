from django import forms

from .models import StudentCard


class RegisterForm(forms.Form):
    id = forms.CharField(label='学籍番号', max_length=7, required=True)
    name = forms.CharField(label='氏名', max_length=64, required=True)
    balance = forms.IntegerField(label='残高', required=True)
    icon = forms.ImageField(label='写真', required=True)
    bio = forms.CharField(label='自由テキスト(128文字まで)', required=True, widget=forms.Textarea(attrs={'rows':4}))


class TopUpForm(forms.Form):
    id = forms.ChoiceField(label='学籍番号', widget=forms.Select, 
                           choices=lambda: [ (card.id, '[{}] {}'.format(card.id, card.name)) for card in StudentCard.objects.all() ], required=True)
    top_up_money = forms.IntegerField(label='チャージ金額', required=True)


class AnalysisForm(forms.Form):
    id = forms.ChoiceField(label='学籍番号', widget=forms.Select, 
                           choices=lambda: [ (card.id, '[{}] {}'.format(card.id, card.name)) for card in StudentCard.objects.all() ], required=True)
