from django import forms

from apps.vote_app.models import Votings


class VoteConfigMeta:
    model = Votings
    fields = [
        'title', 'description', 'image',
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
        'title': forms.TextInput(attrs={
            'class': 'input',
        }),
        'description': forms.Textarea(attrs={
            'class': 'input ultra-wide',
        }),
        'type': forms.RadioSelect,
        'result_see_who': forms.RadioSelect,
        'result_see_when': forms.RadioSelect,
        'end_date': forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'placeholder': 'YYYY-MM-DD HH:MM[:SS]',
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


class ModeledVoteCreateForm(forms.ModelForm):
    class Meta(VoteConfigMeta):
        pass


class ModeledVoteEditForm(forms.ModelForm):
    comment = forms.CharField(required=False, label='Комментарий для модератора',
                              widget=forms.Textarea(attrs={
                                    'class': 'input wide',
                              }))

    class Meta(VoteConfigMeta):
        pass
