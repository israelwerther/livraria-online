from django.shortcuts import render

from .api import get_want_to_read_books

# Create your views here.
def book_list_view(request):
    books = []
    data = get_want_to_read_books()

    if data:
        # Verifica a resposta da API no console
        print(data)  # Imprime a resposta completa
        books = data.get('reading_log_entries', [])
        print(books)  # Verifica se estamos recebendo a lista de livros

    return render(request, 'books/book_list.html', {'books': books})