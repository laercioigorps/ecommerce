from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, RedirectView, UpdateView

from .forms import AddressForm
from .models import Address

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class ListCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.owner = request.user
            address.save()

            redirect_url = request.POST.get("redirect_url", None)
            print("sgdffd---------------------------------sdfs\n")
            print(redirect_url)
            if redirect_url is None:
                redirect_url = reverse("users:list_create_address")
            print("sgdffd---------------------------------sdfs\n")
            print(redirect_url)
            return HttpResponseRedirect(redirect_url)

    def get(self, request):
        addresses = request.user.address_set.all()
        return render(
            request, "users/list_address.html", context={"addresses": addresses}
        )


class CreateAddressView(View):
    def get(self, request):
        form = AddressForm()
        redirect_url = request.GET.get("redirect_url", None)
        return render(
            request,
            "users/address_form.html",
            {"form": form, "redirect_url": redirect_url},
        )


class EditAddressView(LoginRequiredMixin, View):
    def get(self, request, address_id):
        address = Address.objects.get(pk=address_id)
        form = AddressForm(instance=address)
        return render(request, "users/address_form.html", {"form": form})

    def post(self, request, address_id):
        address = Address.objects.get(pk=address_id)
        form = AddressForm(instance=address, data=request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse("users:list_create_address"))
