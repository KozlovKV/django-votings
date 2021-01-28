import copy
from django.urls import reverse
import django.views.generic.edit as generic_edit

from menu_app.view_subclasses import TemplateViewWithMenu
from moderation_app.models import VoteChangeRequest, VoteVariantsChangeRequest
from vote_app.forms import ModeledVoteCreateForm, ModeledVoteEditForm

from vote_app.models import Votings, Votes, VoteVariants
from vote_app.view_vote_one_subclasses import get_variants_context


def get_variants_description_list(request):
    res = []
    for serial_num in range(0, int(request.POST.get('variants_count'))):
        res.append(request.POST.get(f'variant_{serial_num}'))
    return res


class CreateVotingView(generic_edit.CreateView, TemplateViewWithMenu):
    template_name = 'votes/vote_config.html'
    object = None
    model = Votings
    form_class = ModeledVoteCreateForm

    def get_context_data(self, **kwargs):
        context = super(CreateVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': -1,
            'context_url': reverse('vote_create'),
        })
        return context

    def post(self, request, *args, **kwargs):
        post_response = super(CreateVotingView, self).post(self, request, *args, **kwargs)
        self.object.image = self.request.FILES.get('image', None)
        self.object.save()
        self.save_vote_variants()
        return post_response

    def save_vote_variants(self):
        variants_list = get_variants_description_list(self.request)
        variants_count = len(variants_list)
        for serial_number in range(variants_count):
            record = VoteVariants(voting=self.object,
                                  serial_number=serial_number,
                                  description=variants_list[serial_number],
                                  votes_count=0, )
            record.save()


class EditVotingView(generic_edit.UpdateView, TemplateViewWithMenu):
    template_name = 'votes/vote_config.html'
    model = Votings  # and VoteChangeRequest and VoteVariantsChangeRequest
    object = None  # Обрабатываемый объект типа Votings, если не должен изменяеться -> old_object
    old_object = None  # Объект типа Votings, содержит в себе неизменную версию object
    new_request = None  # Объект типа VoteChangeRequest, запрос
    form_class = ModeledVoteEditForm
    pk_url_kwarg = 'voting_id'
    old_variants = []  # Список объектов типа VoteVariants со старыми вариантами
    new_variants = []  # Список строк с новыми вариантами
    new_variants_count = 0
    need_clear_votes = False

    def get_object(self, queryset=None):
        object = super(EditVotingView, self).get_object(queryset)
        self.old_variants = list(VoteVariants.objects.filter(voting=object))
        self.old_variants.sort(key=lambda x: x.serial_number)
        return object

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(EditVotingView, self).get_context_data(**kwargs)
        context.update({
            'voting_id': self.object.pk,
            'can_edit': self.object.can_edit(self.request),
            'context_url': reverse('vote_edit', args=(self.object.pk,)),
            'vote_variants': get_variants_context(self.object),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.old_object = Votings.objects.get(pk=kwargs["voting_id"])
        post_response = super(EditVotingView, self).post(self, request, *args, **kwargs)
        self.new_variants = get_variants_description_list(self.request)
        self.new_variants_count = len(self.new_variants)
        if '_clear' in request.POST:
            self.clear_all_votes()
            if self.is_variants_changed() or self.is_number_of_variants_changed():
                self.save_new_vote_variants()
        if '_save' in request.POST:
            if self.is_title_img_or_desc_changed() or self.is_variants_changed():
                self.save_request()
                self.save_vote_variants()
                self.object = copy.copy(self.old_object)
                self.object.save()
            elif self.is_number_of_variants_changed() or self.is_type_or_anons_changed():
                self.clear_all_votes()
                if self.is_number_of_variants_changed():
                    self.save_new_vote_variants()
        return post_response

    def is_type_or_anons_changed(self):
        return self.request.POST.get('type') != str(self.old_object.type) or \
            (self.request.POST.get('anons_can_vote') == 'on') != self.old_object.anons_can_vote

    def is_title_img_or_desc_changed(self):
        return self.request.POST.get('title') != self.old_object.title or \
               (self.object.image
                if self.request.POST.get('image') == ''
                else self.request.POST.get('image')) != self.old_object.image or \
               self.request.POST.get('description') != self.old_object.description

    def is_variants_changed(self):  # False когда изменилось количество
        need_moderator = False
        if not self.is_number_of_variants_changed():
            for serial_number in range(self.new_variants_count):
                if not need_moderator:
                    need_moderator = self.new_variants[serial_number] != self.old_variants[serial_number].description
        return need_moderator

    def is_number_of_variants_changed(self):
        return self.new_variants_count != len(self.old_variants)

    def save_vote_variants(self):
        for serial_number in range(self.new_variants_count):
            record = VoteVariantsChangeRequest(voting_request=self.new_request,
                                               serial_number=serial_number,
                                               description=self.new_variants[serial_number], )
            record.save()

    def save_new_vote_variants(self):
        VoteVariants.objects.filter(voting=self.object).delete()
        self.object.variants_count = self.new_variants_count
        self.object.save()
        for serial_number in range(self.new_variants_count):
            record = VoteVariants(voting=self.object,
                                  serial_number=serial_number,
                                  description=self.new_variants[serial_number],
                                  votes_count=0, )
            record.save()

    def save_request(self):
        self.new_request = VoteChangeRequest(voting=self.object,
                                             title=self.request.POST.get('title'),
                                             image=self.object.image
                                             if self.request.POST.get('image') == ''
                                             else self.request.FILES.get('image'),
                                             description=self.request.POST.get('description'),
                                             end_date=self.request.POST.get('end_date') if
                                             self.request.POST.get('end_date') != '' else None,
                                             result_see_who=self.request.POST.get('result_see_who'),
                                             result_see_when=self.request.POST.get('result_see_when'),
                                             variants_count=self.request.POST.get('variants_count'),
                                             comment=self.request.POST.get('comment'))
        self.new_request.save()

    def clear_all_votes(self):
        for variant in self.old_variants:
            variant.votes_count = 0
        Votes.objects.filter(voting=self.get_object()).delete()
        self.object.voters_count = 0
        self.object.save()
