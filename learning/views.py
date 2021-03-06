from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Publisher, Book, Author
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import ContactForm
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect



class FirstGenericView(ListView):
    # model  = Publisher
    context_object_name = "my_publisher_list"
    queryset = Publisher.objects.order_by('-name')


# class PublisherDetail(DetailView):
#     model = Publisher

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['book_list'] = Book.objects.all()
#         return context


class AcmeBookList(ListView):

    context_object_name = 'book_list'
    queryset = Book.objects.filter(publisher__name='ACME nhnh Publishing')
    template_name = 'learning/acme_list.html'
    allow_empty = False


class PublisherBookList(ListView):

    template_name = 'learning/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['publisher'] = self.publisher
        return context


class AuthorDetailView(DetailView):

    queryset = Author.objects.all()
    # model = Author

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


class AuthorList(ListView):
    model = Author


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author_list')


class RecordInterest(SingleObjectMixin, View):
    """Records the current user's interest in an author."""
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # Look up the author we're interested in.
        self.object = self.get_object()
        # Actually record interest somehow here!

        return HttpResponseRedirect(reverse('author_detail', kwargs={'pk': self.object.pk}))


class PublisherDetail(SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = "learning/publisher_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.object
        return context

    def get_queryset(self):
        return self.object.book_set.all()
