import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from bir.auth import login_required
from bir.db import get_db

bp = Blueprint('book', __name__)

ALLOWED_COVER_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_COVER_EXTENSIONS


def get_book(id):
    db = get_db()

    book = db.execute('SELECT b.id, title, author, publisher_name, year, rating, category_name,'
                      ' current_page, total_pages, finished, cover FROM book b'
                      ' JOIN category c ON b.category = c.id'
                      ' JOIN publisher p ON b.publisher = p.id'
                      ' WHERE b.id = ?', (id,)).fetchone()

    return book


@bp.route('/')
def index():
    db = get_db()
    books = db.execute(
        'SELECT b.id, title, rating, author, publisher_name, year, review, category_name, current_page, total_pages, finished, cover'
        ' FROM book b JOIN publisher p ON b.publisher = p.id'
        ' JOIN category c ON b.category = c.id'
        ' ORDER by created DESC'
    ).fetchall()

    book_ratings = []
    for book in books:
        rating = {
            'rating-fill': '*' * book['rating'],
            'rating-empty': '*' * (5 - book['rating'])
        }

        book_ratings.append(rating)

    return render_template('books/index.html', books=books, book_ratings=book_ratings)


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_book():
    db = get_db()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        year = request.form['year']
        rating = request.form['rating']
        category = request.form['category']
        current_page = request.form['current-page']
        total_pages = request.form['total-pages']
        cover = ''

        if 'cover-file' not in request.files:
            cover = ''
        else:
            print("File found")
            cover_file = request.files['cover-file']
            if cover_file.filename != '' and allowed_filename(cover_file.filename):
                file_extension = cover_file.filename.rsplit('.', 1)[-1]
                filename = secure_filename(title) + '.' + file_extension
                #filename = secure_filename(cover_file.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                tmp_index = 0

                while os.path.exists(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], filename)):
                    filename = "{0}{1}".format(tmp_index, filename)
                    tmp_index += 1

                cover_file.save(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], filename))
                cover = filename
            elif cover_file.filename != '':
                flash("Allowed image types are: png, jpg, jpeg and gif")

        publisher_id = db.execute('SELECT id FROM publisher WHERE publisher_name = ?', (publisher,)).fetchone()
        category_id = db.execute('SELECT id FROM category WHERE category_name = ?', (category,)).fetchone()

        if publisher_id is None:
            db.execute(
                'INSERT INTO publisher (publisher_name)'
                ' VALUES (?)',
                (publisher,)
            )
            db.commit()
            publisher_id = db.execute('SELECT id FROM publisher WHERE publisher_name = ?', (publisher,)).fetchone()

        error = None

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO book (title, author, publisher, year, rating, category, current_page, total_pages, cover)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, author, publisher_id['id'], year, rating, category_id['id'], current_page, total_pages, cover)
            )
            db.commit()
            return redirect(url_for('index'))

    publishers = db.execute('SELECT * FROM publisher').fetchall()
    categories = db.execute('SELECT * FROM category').fetchall()
    return render_template('books/add.html', publishers=publishers, categories=categories)


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit_book(id):
    db = get_db()
    book = get_book(id)

    if book is None:
        abort(404, "Book id {0} doesn't exist.".format(id))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        year = request.form['year']
        rating = request.form['rating']
        category = request.form['category']
        current_page = request.form['current-page']
        total_pages = request.form['total-pages']
        if (request.form.get('finished') != None):
            finished = 'True'
        else:
            finished = 'False'

        if 'cover-file' in request.files:
            cover_file = request.files['cover-file']
            if cover_file.filename != '' and allowed_filename(cover_file.filename):
                file_extension = cover_file.filename.rsplit('.', 1)[-1]
                filename = secure_filename(title) + '.' + file_extension
                #filename = secure_filename(cover_file.filename)
                basedir = os.path.abspath(os.path.dirname(__file__))
                tmp_index = 0

                while os.path.exists(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], filename)):
                    filename = "{0}{1}".format(tmp_index, filename)
                    tmp_index += 1

                cover_file.save(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], filename))
                db.execute(
                    'UPDATE book SET cover = ? WHERE id = ?',
                    (filename, id)
                )
                db.commit()
            elif cover_file.filename != '':
                flash("Allowed image types are: png, jpg, jpeg and gif")

        publisher_id = db.execute('SELECT id FROM publisher WHERE publisher_name = ?', (publisher,)).fetchone()
        category_id = db.execute('SELECT id FROM category WHERE category_name = ?', (category,)).fetchone()

        if publisher_id is None:
            db.execute(
                'INSERT INTO publisher (publisher_name)'
                ' VALUES (?)',
                (publisher,)
            )
            db.commit()
            publisher_id = db.execute('SELECT id FROM publisher WHERE publisher_name = ?', (publisher,)).fetchone()

        error = None

        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE book SET title = ?, author = ?, publisher = ?, year = ?,'
                ' rating = ?, category = ?, current_page = ?, total_pages = ?,'
                ' finished = ? WHERE id = ?',
                (title, author, publisher_id['id'], year, rating, category_id['id'], current_page, total_pages, finished, id)
            )
            db.commit()
            return redirect(url_for('index'))

    publishers = db.execute('SELECT * FROM publisher').fetchall()
    categories = db.execute('SELECT * FROM category').fetchall()
    return render_template('books/edit.html', book=book, publishers=publishers, categories=categories)

@bp.route('/<int:id>/delete')
@login_required
def delete_book(id):
    book = get_book(id)
    if book['cover'] != '':
        filepath = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            current_app.config['UPLOAD_FOLDER'],
            book['cover']
        )
        if os.path.exists(filepath):
            os.remove(filepath)

    db = get_db()
    db.execute('DELETE FROM book WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('index'))
