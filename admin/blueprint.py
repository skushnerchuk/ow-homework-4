import os

from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError, OperationalError

from models import Category, Product
from app import app, db
from utils import is_correct_ext


ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']


admin = Blueprint('admin', __name__, template_folder='templates')


def get_categories_choices():
    choices = []
    items = Category.query.all()
    for item in items:
        choices.append({'id': item.id, 'name': item.name})
    return choices


def add_product(form):
    product = Product()
    product.name = form['name']
    product.category = form['category']
    product.short_description = form['short_description']
    product.description = form['description']
    product.price = form['price']
    file = request.files['file']
    if file and is_correct_ext(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product.image = '/static/uploads/{}'.format(filename)
    db.session.add(product)
    db.session.commit()


def add_category():
    try:
        category = Category()
        category.name = request.form['new_category']
        db.session.add(category)
        db.session.commit()
    except (IntegrityError, OperationalError) as ex:
        # Если такая категория уже существует, игнорируем
        if ex.orig.args[0] == 1062:
            db.session.rollback()
        else:
            raise ex


@admin.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if 'new_category' in request.form:
            add_category()
        else:
            add_product(request.form)
    return render_template('admin/index.html', categories=get_categories_choices())
