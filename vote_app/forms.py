from django import forms

from vote_app.models import Votings


class ModeledVoteCreateForm(forms.ModelForm):
    class Meta:
        model = Votings
        fields = [
            'title', 'image', 'description',
            'type', 'anons_can_vote',
            'result_see_who', 'result_see_when',
            'end_date', 'variants_count', 'author',
        ]
        labels = {
            'title': 'Заголовок',
            'image': 'Картинка',
            'description': 'Описание',
            'type': 'Тип голосования',
            'anons_can_vote': 'Разрешить голосовать анонимам',
            'result_see_who': 'Кому видны результаты',
            'result_see_when': 'Когда видные результаты',
            'end_date': 'Дата окончания (пусто - бессрочно)',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'style': 'width: 95%',
            }),
            'type': forms.RadioSelect,
            'result_see_who': forms.RadioSelect,
            'result_see_when': forms.RadioSelect,
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime',
            }),
            'variants_count': forms.NumberInput(attrs={
                'type': 'hidden',
                'id': 'variants_count',
            }),
            'author': forms.TextInput(attrs={
                'type': 'hidden',
                'id': 'author',
            }),
        }


class ModeledVoteEditForm(forms.ModelForm):
    comment = forms.CharField(required=False, label='Комментарий для модератора',
                              widget=forms.Textarea(attrs={
                                  'style': 'width: 95%',
                              }))

    class Meta:
        model = Votings
        fields = [
            'title', 'image', 'description',
            'type', 'anons_can_vote',
            'result_see_who', 'result_see_when',
            'end_date',
        ]
        labels = {
            'title': 'Заголовок',
            'image': 'Картинка',
            'description': 'Описание',
            'type': 'Тип голосования',
            'anons_can_vote': 'Разрешить голосовать анонимам',
            'result_see_who': 'Кому видны результаты',
            'result_see_when': 'Когда видные результаты',
            'end_date': 'Дата окончания (пусто - бессрочно)',
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'style': 'width: 95%',
            }),
            'type': forms.RadioSelect,
            'result_see_who': forms.RadioSelect,
            'result_see_when': forms.RadioSelect,
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime',
            }),
        }
