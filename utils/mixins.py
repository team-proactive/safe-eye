from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.http import Http404


class Custom404Mixin:
    custom_404_message = None

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Http404:
            message = self.custom_404_message or "페이지를 찾을 수 없습니다."
            context = {"message": message}
            return render(request, "custom_404.html", context, status=404)
        

class UserIsContentAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        content_object = obj.content_object
        return content_object.author == self.request.user