from django import forms

from vote_app.models import Votings


class ModeledVoteCreateForm(forms.ModelForm):
    class Meta:
        model = Votings
        fields = [
            'Title', 'Image', 'Description',
            'Type', 'Anons_can_vote',
            'Result_see_who', 'Result_see_when',
            'End_date', 'Variants_count',
        ]
        labels = {
            'Title': 'Заголовок',
            'Image': 'Картинка',
            'Description': 'Описание',
            'Type': 'Тип голосования',
            'Anons_can_vote': 'Разрешить голосовать анонимам',
            'Result_see_who': 'Кому видны результаты',
            'Result_see_when': 'Когда видные результаты',
            'End_date': 'Дата окончания (пусто - бессрочно)',
        }
        widgets = {
            'Description': forms.Textarea(attrs={
                'style': 'width: 95%',
            }),
            'Type': forms.RadioSelect,
            'Result_see_who': forms.RadioSelect,
            'Result_see_when': forms.RadioSelect,
            'End_date': forms.DateTimeInput(attrs={
                'type': 'datetime',
            }),
            'Variants_count': forms.NumberInput(attrs={
                'type': 'hidden',
                'id': 'variants_count',
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
            'Title', 'Image', 'Description',
            'Type', 'Anons_can_vote',
            'Result_see_who', 'Result_see_when',
            'End_date',
        ]
        labels = {
            'Title': 'Заголовок',
            'Image': 'Картинка',
            'Description': 'Описание',
            'Type': 'Тип голосования',
            'Anons_can_vote': 'Разрешить голосовать анонимам',
            'Result_see_who': 'Кому видны результаты',
            'Result_see_when': 'Когда видные результаты',
            'End_date': 'Дата окончания (пусто - бессрочно)',
        }
        widgets = {
            'Description': forms.Textarea(attrs={
                'style': 'width: 95%',
            }),
            'Type': forms.RadioSelect,
            'Result_see_who': forms.RadioSelect,
            'Result_see_when': forms.RadioSelect,
            'End_date': forms.DateTimeInput(attrs={
                'type': 'datetime',
            }),
        }
