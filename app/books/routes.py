from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .forms import Booksearchform
from app.models import Books
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
                    doc['key'] = (doc['key']).replace("/works/", "")

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
                        'id' : doc['isbn'][0],
                        'key' : doc['key'],
                        'cover_edition_key' : doc['cover_edition_key'],
                        'title' : doc['title'],
                        'cover_id' : doc['cover_i'],
                        'author' : doc['author_name'][0]
                    })

                                    
    return render_template('book_search.html', form=form, book_info=book_info, docs_with_covers=docs_with_covers)


@books.route('/add_to_wishlist/<book_key>')
def add_to_wishlist(book_id):
    form = Booksearchform()
    check = Books.query.all()
    print(check)
    if book_id in check:
        pass
    else:
        url = f'http://openlibrary.org/search.json?q={book_key}'
        response = requests.get(url) 
        data = response.json()
        print(data)
    #     cover_url = response.json()['docs'][0]['cover_i']   
    #     book_info = {
    #         'id': response.json()['docs'][0]['isbn'][0],
    #         'cover_edition_key' : response.json()['docs'][0]['cover_edition_key'],
    #         'title' : response.json()['docs'][0]['title'],
    #         'author' : response.json()['docs'][0]['author_name'][0],
    #         'cover_id' : f"https://covers.openlibrary.org/b/id/{cover_url}-L.jpg"
    #     }

    #     id = book_info['id']
    #     cover_edition_key = book_info['cover_edition_key']
    #     title = book_info['title']
    #     author = book_info['author']
    #     cover_img = book_info['cover_id']

    #     new_book = Books(id, key, title, author, cover_img)
    #     new_book.save_to_db()
        
    # book = Books.query.get(book_id)
    # if book:
    #     current_user.add(book)
    #     flash(f'Successfully added {book.title} to your wishlist!', 'success')
    # else:
    #     flash('Error!', 'danger')

    return render_template('book_search.html', form=form)

@books.route('/book_details/<book_key>')
def book_details(book_key):
    url = f"https://openlibrary.org/works/{book_key}.json"
    response = requests.get(url)
    data = response.json()
    print(data)
    cover_id = data['covers'][0]
    print(cover_id)
    key = data['key'].replace("/works/", "")
    print(key)
    book_details = {
        'title' : data['title'],
        'cover_img' : f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg",
        'key' : key,
        'subjects' : data['subjects'][0],
        'description' : data['description']['value']
    }
    print(book_details)
    return render_template('book_details.html', book_details=book_details)