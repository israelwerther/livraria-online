from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'core/index.html'
    
    def test_func(self):
        return self.request.user.is_superuser