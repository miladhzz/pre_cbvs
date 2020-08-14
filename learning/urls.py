from django.urls import path
from .views import (
    FirstGenericView, 
    AcmeBookList, 
    PublisherBookList, 
    AuthorDetailView, 
    AuthorList,
    AuthorCreate, 
    AuthorDelete, 
    AuthorUpdate
)

urlpatterns = [
    path('', FirstGenericView.as_view()),
    path('acme/', AcmeBookList.as_view()),
    path('books/<publisher>/', PublisherBookList.as_view()),
    path('authors/', AuthorList.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('author/add/', AuthorCreate.as_view(), name='author_add'),
    path('author/<int:pk>/', AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', AuthorDelete.as_view(), name='author_delete'),
]
