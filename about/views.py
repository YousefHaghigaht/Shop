from django.views.generic import TemplateView


class AboutUsView(TemplateView):
    template_name = 'about/about.html'


class CantactUsView(TemplateView):
    template_name = 'about/contact-us.html'

