# -*- coding: utf-8 -*-

import os

from flask_migrate import Migrate, migrate, upgrade, init

from application import app, db
import models


migrations = Migrate(app, db)


def prepare_database():
    if not os.path.exists('migrations'):
        with app.app_context():
            init()
            migrate()
            upgrade()


@app.route('/upgrade_database', methods=['GET'])
def upgrade_database():
    try:
        with app.app_context():
            migrate()
            upgrade()
        return 'Upgrade OK', 200
    except Exception as ex:
        return 'Upgrade error:{}'.format(ex), 500

