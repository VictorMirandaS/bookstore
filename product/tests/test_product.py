import pytest
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
    assert data['description'] == product.description
    assert float(data['price']) == float(product.price)
    assert data['stock'] == product.stock