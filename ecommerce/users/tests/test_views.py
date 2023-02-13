import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from ecommerce.users.forms import UserAdminChangeForm
from ecommerce.users.models import Address, User
from ecommerce.users.tests.factories import UserFactory
from ecommerce.users.views import UserRedirectView, UserUpdateView, user_detail_view

from ..forms import AddressForm

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        # Initialize the form
        form = UserAdminChangeForm()
        form.cleaned_data = {}
        form.instance = user
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == ["Information successfully updated"]


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserRedirectView()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = user_detail_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()

        response = user_detail_view(request, username=user.username)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"


def test_list_address_for_anonymous_user(client, user):
    response = client.get(reverse("users:list_create_address"))
    assert response.status_code == 302


def test_list_address_for_valid_user(client, user):
    client.force_login(user)
    user.address_set.create(
        line_1="line 1 address 1",
        line_2="line 2 address 1",
        city="city 1",
        state="state 1",
        postal_code="postal_code 1",
        country_code="country_code 1",
    )

    user.address_set.create(
        line_1="line 1 address 2",
        line_2="line 2 address 2",
        city="city 2",
        state="state 2",
        postal_code="postal_code 2",
        country_code="country_code 2",
    )

    response = client.get(reverse("users:list_create_address"))

    assert response.status_code == 200
    assertTemplateUsed(response, "users/list_address.html")
    assert len(response.context["addresses"]) == 2
    assert response.context["addresses"][0].line_1 == "line 1 address 1"
    assert response.context["addresses"][1].line_1 == "line 1 address 2"


def test_add_address_for_anonymour_user(client):
    response = client.post(
        reverse("users:list_create_address"),
        data={
            "line_1": "address line 1",
            "line_2": "address line 1",
            "city": "city",
            "state": "state",
            "postal_code": "postal_code",
            "country_code": "US",
        },
    )
    assert response.status_code == 302
    assert Address.objects.count() == 0


def test_add_address_for_valid_user(client, user):
    client.force_login(user)
    response = client.post(
        reverse("users:list_create_address"),
        data={
            "line_1": "address line 1",
            "line_2": "address line 1",
            "city": "city",
            "state": "state",
            "postal_code": "postal_code",
            "country_code": "US",
        },
    )
    addresses = Address.objects.all()
    assertRedirects(response, reverse("users:list_create_address"))
    assert addresses.count() == 1
    assert addresses.first().owner == user


def test_access_edit_address_page_with_anonymous_user(client, user):
    address = user.address_set.create(
        line_1="line 1 address 2",
        line_2="line 2 address 2",
        city="city 2",
        state="state 2",
        postal_code="postal_code 2",
        country_code="country_code 2",
    )
    response = client.get(
        reverse("users:edit_address", kwargs={"address_id": address.id})
    )
    assert response.status_code == 302


def test_access_edit_address_page_with_valid_user(client, user):
    client.force_login(user)
    address = user.address_set.create(
        line_1="line 1 address 2",
        line_2="line 2 address 2",
        city="city 2",
        state="state 2",
        postal_code="postal_code 2",
        country_code="country_code 2",
    )
    response = client.get(
        reverse("users:edit_address", kwargs={"address_id": address.id})
    )
    assert response.status_code == 200
    assertTemplateUsed(response, "users/address_form.html")
    assert isinstance(response.context["form"], AddressForm)
    print(response.context["form"].instance)
    assert response.context["form"].instance.line_1 == "line 1 address 2"


def test_edit_address_with_valid_user(client, user):
    client.force_login(user)
    address = user.address_set.create(
        line_1="line 1 address",
        line_2="line 2 address",
        city="city",
        state="state",
        postal_code="postal_code",
        country_code="country_code",
    )
    response = client.post(
        reverse("users:edit_address", kwargs={"address_id": address.id}),
        data={
            "line_1": "line 1 address edited",
            "line_2": "line 2 address edited",
            "city": "city",
            "state": "state",
            "postal_code": "postal_code",
            "country_code": "country_code",
        },
    )
    assert response.status_code == 302
    assertRedirects(response, reverse("users:list_create_address"))
    assert Address.objects.count() == 1
    assert Address.objects.first().line_1 == "line 1 address edited"


def test_create_address_with_redirect_url_paramether(client, user):
    client.force_login(user)
    response = client.post(
        reverse("users:list_create_address"),
        data={
            "line_1": "address line 1",
            "line_2": "address line 1",
            "city": "city",
            "state": "state",
            "postal_code": "postal_code",
            "country_code": "US",
            "redirect_url": reverse("shop:select_address"),
        },
    )
    assertRedirects(response, reverse("shop:select_address"))


def test_get_create_address_page_with_redirect_url_paramether_has_context(client, user):
    client.force_login(user)
    response = client.get(
        f'{reverse("users:create_address")}?redirect_url={reverse("shop:select_address")}'
    )
    assert response.context["redirect_url"] == reverse("shop:select_address")
