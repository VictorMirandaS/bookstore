import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from product.factories import ProductFactory
from product.serializers import ProductSerializer


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='senha123')


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_product_creation():
    product = ProductFactory()
    assert product.id is not None
    assert product.name != ""


@pytest.mark.django_db
def test_product_serializer():
    product = ProductFactory()
    serializer = ProductSerializer(product)
    data = serializer.data
    assert data['name'] == product.name


@pytest.mark.django_db
def test_list_products(auth_client):
    ProductFactory.create_batch(3)
    response = auth_client.get('/api/products/')
    assert response.status_code == 200
    assert response.data['count'] == 3
    assert len(response.data['results']) == 3


@pytest.mark.django_db
def test_create_product(auth_client):
    payload = {
        'name': 'Livro Python',
        'description': 'Um livro sobre Python',
        'price': '49.90',
        'stock': 10
    }
    response = auth_client.post('/api/products/', payload, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'Livro Python'


@pytest.mark.django_db
def test_list_products_requires_authentication():
    client = APIClient()
    response = client.get('/api/products/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_obtain_token(user):
    client = APIClient()
    response = client.post('/api-token-auth/', {
        'username': 'testuser',
        'password': 'senha123'
    })
    assert response.status_code == 200
    assert 'token' in response.data


@pytest.mark.django_db
def test_access_with_token(user):
    client = APIClient()
    token_response = client.post('/api-token-auth/', {
        'username': 'testuser',
        'password': 'senha123'
    })
    token = token_response.data['token']

    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = client.get('/api/products/')
    assert response.status_code == 200