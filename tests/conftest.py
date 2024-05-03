import pytest

from ..project.app import create_app,db

@pytest.fixture()
def app():
    app = create_app()
    
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
    
    with app.app_context():
        db.create_all()
        
        yield app
        
@pytest.fixture()
def client(app):
    return app.test_client()