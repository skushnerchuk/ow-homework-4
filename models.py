from app import db


class Category(db.Model):
    """Категория продуктов"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Category id: {}, name: {}>'.format(self.id, self.name)


class Product(db.Model):
    """Продукт"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.Integer)
    price = db.Column(db.Integer)
    description = db.Column(db.Text)
    short_description = db.Column(db.Text)
    image = db.Column(db.String(512))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Product id: {}, name: {}>'.format(self.id, self.name)
