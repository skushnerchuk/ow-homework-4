from flask import render_template, request, session, redirect

from app import app, db
from models import Category, Product
from admin.blueprint import admin

db.create_all()
app.register_blueprint(admin, url_prefix='/admin')


def add_product_to_session(product_id):
    """
    Добавление продукта в сессию. Используется для реализации корзины
    и создания заказа без регистрации пользователя
    """
    if 'cart' not in session:
        session['cart'] = {}
    if product_id in session['cart']:
        session['cart'][product_id] += 1
    else:
        session['cart'][product_id] = 1
    session.modified = True


@app.route('/', methods=['GET'])
def index():
    """Индексная страница. На ней показываем продукты всех категорий"""
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('index.html', categories=categories, products=products)


@app.route('/categories/<category_id>', methods=['GET'])
def category(category_id):
    """Показ продуктов по категориям"""
    categories = Category.query.all()
    products = Product.query.filter(Product.category == category_id).all()
    return render_template('index.html', categories=categories, products=products)


@app.route('/product/<product_id>', methods=['GET', 'POST'])
def product(product_id):
    """Показ деталей по продукту + добавление его в корзину"""
    categories = Category.query.all()
    if request.method == 'POST':
        form = request.form
        add_product_to_session(form['id'])
        return redirect('/', 302)

    product_info = Product.query.filter(Product.id == product_id).first()
    if not product_info:
        return redirect('/', 302)
    return render_template('product.html', categories=categories, product=product_info)


def process_cart_requests():
    if 'reset' in request.form:
        # Сброс всей сессии
        session.clear()
        return redirect('/', 302)

    if 'delete' in request.form and request.form['id'] in session['cart']:
        # Удаление указанного продукта из корзины
        del session['cart'][str(request.form['id'])]
        session.modified = True


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """Корзина заказа"""
    if 'cart' not in session:
        return render_template('cart.html', carst='Cart is empty')

    if request.method == 'POST':
        process_cart_requests()

    cart_items = []
    total_amount = 0
    # Формируем данные для таблицы заказа
    for item in session['cart']:
        product = Product.query.filter(Product.id == item).first()
        total_amount += product.price * session['cart'][item]
        cart_items.append({
            'name': product.name,
            'count': session['cart'][item],
            'price': product.price,
            'id': product.id
        })

    return render_template('cart.html', cart=cart_items, total=total_amount)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
