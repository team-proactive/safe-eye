from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Tag, Status
from .mixins import UserIsContentAuthorMixin, Custom404Mixin
from django.core.exceptions import PermissionDenied

class TagListView(ListView):
    model = Tag


class TagDetailView(Custom404Mixin, DetailView):
    model = Tag
    custom_404_message = "해당 태그를 찾을 수 없습니다."


class TagCreateView(CreateView):
    model = Tag
    fields = ['tag_type', 'tag_content', 'tag_id', 'content_type', 'object_id']
    success_url = reverse_lazy('tag_list')


class TagUpdateView(UserIsContentAuthorMixin, UpdateView):
    model = Tag
    fields = ['tag_type', 'tag_content', 'tag_id', 'content_type', 'object_id']
    success_url = reverse_lazy('tag_list')


class TagDeleteView(UserIsContentAuthorMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('tag_list')


class StatusListView(ListView):
    model = Status


class StatusDetailView(Custom404Mixin, DetailView):
    model = Status
    custom_404_message = "해당 상태를 찾을 수 없습니다."


class StatusCreateView(CreateView):
    model = Status
    fields = ['available', 'content_type', 'object_id']
    success_url = reverse_lazy('status_list')


class StatusUpdateView(UserIsContentAuthorMixin, UpdateView):
    model = Status
    fields = ['available', 'content_type', 'object_id']
    success_url = reverse_lazy('status_list')


class StatusDeleteView(UserIsContentAuthorMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('status_list')


class SetContentAuthorMixin:
    def form_valid(self, form):
        content_object = form.instance.content_object
        
        # 현재 사용자가 연결된 모델(예: Post)의 작성자인지 확인
        if content_object.author != self.request.user:
            # 권한이 없는 경우 적절한 예외 또는 에러 응답 반환
            raise PermissionDenied()
        
        response = super().form_valid(form)
        content_object.author = self.request.user
        content_object.save()
        return response