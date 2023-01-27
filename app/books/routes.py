from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .forms import Booksearchform
from app.models import Books, Favorites, Wishlist, Dislikes
import requests

books = Blueprint('books', __name__, template_folder='books_templates')

@books.route('/book_search', methods=['GET', 'POST'])
def search_books():
    form = Booksearchform()
    book_info = []
    docs_with_covers = []
    if request.method == 'POST':
        if form.validate():
            search = form.search.data
            url = f'http://openlibrary.org/search.json?q={search}'
            response = requests.get(url)
            if response.ok == True:
                data = response.json()
                docs = data['docs']
                limit_docs = docs[0:20]

                # get dictionaries with cover_img id
                for doc in limit_docs:
                    for i in doc:
                        if i == 'cover_i':
                            docs_with_covers.append(doc)
                        else:
                            pass

                # change cover_id to url for cover_img
                for doc in docs_with_covers:
                    doc['cover_i'] = "https://covers.openlibrary.org/b/id/{cover_i}-L.jpg".format(**doc)

                # api call to get description
                # id = doc['cover_edition_key']
                # url = f'https://openlibrary.org/works/{id}.json'
                # response = requests.get(url)
                # if response.ok == True:
                #     data = response.json()
                #     description = data
                #     print(description)

                for doc in docs_with_covers:
                    book_info.append({
                        'key' : doc['isbn'][0],
                        'id' : doc['cover_edition_key'],
                        'title' : doc['title'],
                        'cover_id' : doc['cover_i'],
                        'author' : doc['author_name'][0]
                    })

                                    
    return render_template('book_search.html', form=form, book_info=book_info, docs_with_covers=docs_with_covers)

@books.route('/add_wishlist/<book>/<books_id>')
def add_wishlist(book, books_id):
    form = Booksearchform()
    check = Wishlist.query.all()
    if books_id in check:
        print("Already added")
    else:
        url = f'http://openlibrary.org/search.json?q={book}'
        response = requests.get(url) 
        cover_url = response.json()['docs'][0]['cover_i']   
        book_info = {
            'key': response.json()['docs'][0]['isbn'][0],
            'id' : response.json()['docs'][0]['cover_edition_key'],
            'title' : response.json()['docs'][0]['title'],
            'cover_id' : f"https://covers.openlibrary.org/b/id/{cover_url}-L.jpg",
            'author' : response.json()['docs'][0]['author_name'][0]
        }
        key = book_info['key']
        id = book_info['id']
        title = book_info['title']
        cover_img = book_info['cover_id']
        author = book_info['author']
        new_book = Books(id, key, title, author, cover_img)

        new_book.save_to_db()
        print('success')
        return redirect(url_for('books.search_books'))

    return render_template('book_search.html')
