import pytest
from rest_framework.test import APIClient
from product.factories import ProductFactory
from product.serializers import ProductSerializer

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
def test_list_products():
    ProductFactory.create_batch(3)
    client = APIClient()
    response = client.get('/api/products/')
    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_create_product():
    client = APIClient()
    payload = {
        'name': 'Livro Python',
        'description': 'Um livro sobre Python',
        'price': '49.90',
        'stock': 10
    }
    response = client.post('/api/products/', payload, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'Livro Python'