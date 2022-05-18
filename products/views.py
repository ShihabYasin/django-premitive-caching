from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, View

from .models import Product


class HomePageView(View):
    template_name = 'products/home.html'

    def get(self, request):
        product_objects = cache.get('product_objects')

        if product_objects is None:
            product_objects = Product.objects.all()
            cache.set('product_objects', product_objects)

        context = {
            'products': product_objects
        }

        return render(request, self.template_name, context)


class ProductCreateView(CreateView):
    model = Product
    fields = ['title', 'price']
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('home')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['title', 'price']
    template_name = 'products/product_update.html'

    # we overrode the post method for testing purposes
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        Product.objects.filter(id=self.object.id).update(
            title=request.POST.get('title'),
            price=request.POST.get('price')
        )
        return HttpResponseRedirect(reverse_lazy('home'))


def invalidate_cache(request):
    cache.delete('product_objects')
    url = reverse_lazy('home')
    return HttpResponseRedirect(redirect_to=url)
