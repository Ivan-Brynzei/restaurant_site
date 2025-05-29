import pytest
from django.urls import reverse
from menu.models import Dish, Category

@pytest.fixture
def category(db):
    return Category.objects.create(name="Супи")

@pytest.fixture
def dish(category):
    return Dish.objects.create(name="Борщ", price=100, category=category)

@pytest.mark.django_db
def test_home_view(client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]

@pytest.mark.django_db
def test_menu_view(client, dish):
    url = reverse("menu")
    response = client.get(url)
    assert response.status_code == 200
    assert dish.name in response.content.decode()

@pytest.mark.django_db
def test_add_to_cart_ajax(client, dish):
    url = reverse("add_to_cart_ajax")
    response = client.post(url, {"dish_id": dish.id},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    assert response.status_code == 200
    assert response.json()["success"] is True
    session = client.session
    assert str(dish.id) in session["cart"]

@pytest.mark.django_db
def test_checkout_post(client, dish, settings):
    session = client.session
    session["cart"] = {str(dish.id): 2}
    session.save()

    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.ADMIN_EMAIL = "admin@example.com"

    response = client.post(reverse("checkout"), {
        "name": "Іван",
        "phone": "123456789",
        "address": "Київ"
    })
    assert response.status_code == 200
    assert "checkout_success" in response.templates[0].name
    assert "cart" not in client.session
