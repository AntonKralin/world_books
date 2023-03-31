from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseNotFound
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .models import Author, Book, BookInstance, Genre, Language, Status
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthorsForm
from django.urls import reverse_lazy


# Create your views here.
def index(request:HttpRequest) -> HttpResponse:
    num_book  = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    
    num_instance_available = BookInstance.objects.filter(status=2).count()
    num_authors = Author.objects.count()
    
    num_visits = request.session.get('num_visit',0)
    request.session['num_visit'] = num_visits + 1
    
    return render(request, 'index.html',
                  context={'num_instance': num_instance,
                           'num_instance_available': num_instance_available,
                           'num_book': num_book,
                           'num_authors': num_authors,
                           'num_visits': num_visits})

def authors_add(request):
    author = Author.objects.all()
    authors_form = AuthorsForm()
    return render(request, 'authors_add.html',
                  {'form': authors_form, 'author': author})


def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add')
    

def delete1(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add")
    except Author.DoesNotExist:
        return HttpResponseNotFound('<h2>Не найден автор</h2>')
    

def edit1(request, id):
    author = Author.objects.get(id=id)
    print(request.POST.get('first_name'))
    if request.method == "POST":
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        author.save()
        return HttpResponseRedirect('/authors_add')
    else:
        return render(request, f'edit1.html', {"author": author})
    
    

class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 3


class BookDetailView(generic.ListView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Book.objects.filter(id=int(pk))


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4
    template_name = 'author_list.html'
    
    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Универсальный класс представления списка книг, находящихся в заказе у текущего пользователя"""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status='2').order_by('due_back')
    
    
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
    template_name = 'book_form.html'
    

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')
    template_name = 'book_form.html'
    

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    template_name = 'book_confirm_delete.html'