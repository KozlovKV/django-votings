from django import forms

from vote_app.models import Votings


class VoteConfigForm(forms.Form):
    title = forms.CharField(max_length=256, empty_value='Заголовок')
    image = forms.ImageField()
    description = forms.CharField(empty_value='Описание')
    ONE = 0
    MANY = 1
    VOTING_TYPE = [
        (ONE, 'Одиночный выбор'),
        (MANY, 'Множественный выбор'),
    ]
    type = forms.ChoiceField(choices=VOTING_TYPE, widget=forms.RadioSelect)
    ALL = 0
    VOTED = 1
    SEE_WHO_CHOICES = [
        (ALL, 'Всем'),
        (VOTED, 'Проголосовавшим'),
    ]
    see_who = forms.ChoiceField(choices=SEE_WHO_CHOICES, widget=forms.RadioSelect)
    ANYTIME = 0
    BY_TIMER = 1
    SEE_WHEN_CHOICES = [
        (ANYTIME, 'В любой момент'),
        (BY_TIMER, 'После истечения времени голосования'),
    ]
    when_see = forms.ChoiceField(choices=SEE_WHEN_CHOICES, widget=forms.RadioSelect)
    anons_can = forms.BooleanField()

    # Elements names
    title.label = 'Заголовок голосования'
    image.label = 'Загрузить изображение'
    description.label = 'Описание'
    type.label = 'Тип голосования'
    see_who.label = 'Кому видны результаты?'
    when_see.label = 'Когда видны результаты?'
    anons_can.label = 'Анонимы могут голосовать'


class ModeledVoteCreateForm(forms.ModelForm):
    class Meta:
        model = Votings
        fields = [
            'Title', 'Image', 'Description',
            'Type', 'AnonsCanVote',
            'ResultSeeWho', 'ResultSeeWhen',
            'EndDate',
        ]
        labels = {
            'Title': 'Заголовок',
            'Image': 'Картинка',
            'Description': 'Описание',
            'Type': 'Тип голосования',
            'AnonsCanVote': 'Разрешить голосовать анонимам',
            'ResultSeeWho': 'Кому видны результаты',
            'ResultSeeWhen': 'Когда видные результаты',
            'EndDate': 'Дата окончания (пусто - бессрочно)',
        }
        widgets = {
            'Description': forms.Textarea(attrs={
                'style': 'width: 95%',
            }),
            'Type': forms.RadioSelect,
            'ResultSeeWho': forms.RadioSelect,
            'ResultSeeWhen': forms.RadioSelect,
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
            'Type', 'AnonsCanVote',
            'ResultSeeWho', 'ResultSeeWhen',
            'EndDate',
        ]
        labels = {
            'Title': 'Заголовок',
            'Image': 'Картинка',
            'Description': 'Описание',
            'Type': 'Тип голосования',
            'AnonsCanVote': 'Разрешить голосовать анонимам',
            'ResultSeeWho': 'Кому видны результаты',
            'ResultSeeWhen': 'Когда видные результаты',
            'EndDate': 'Дата окончания (пусто - бессрочно)',
        }
        widgets = {
            'Description': forms.Textarea(attrs={
                'style': 'width: 95%',
            }),
            'Type': forms.RadioSelect,
            'ResultSeeWho': forms.RadioSelect,
            'ResultSeeWhen': forms.RadioSelect,
        }