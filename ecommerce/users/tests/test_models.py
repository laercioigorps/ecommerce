from ecommerce.users.models import User


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_add_address_to_user(user):
    address = user.address_set.create(
        line_1="2101 Main St",
        line_2="house",
        city="Victoria",
        state="Virginia",
        postal_code="23974",
        country_code="US",
    )
    assert user.address_set.count() == 1
    assert str(address) == "2101 Main St, house | Victoria, Virginia, 23974 - US"

    address = user.address_set.create(
        line_1="32 Foreman Dr",
        line_2="house",
        city="Glen Carbon",
        state="Illinois",
        postal_code="62034",
        country_code="US",
    )
    assert user.address_set.count() == 2
    assert str(address) == "32 Foreman Dr, house | Glen Carbon, Illinois, 62034 - US"
