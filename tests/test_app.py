import os

os.environ.setdefault('STUDENT', 'Test Student')
os.environ.setdefault('COLLEGE', 'Test College')

from app import celsius_to_fahrenheit, create_app


def test_conversion_points():
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(-40) == -40


def test_home_page_and_database_write():
    app = create_app(
        {
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        }
    )
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>TempConverter</title>' in response.data
    assert b'Test Student' in response.data
    assert b'Test College' in response.data

    response = client.post('/', data={'celsius': '20', 'submit': 'Convert'})
    assert response.status_code == 200
    assert b'68.0' in response.data
