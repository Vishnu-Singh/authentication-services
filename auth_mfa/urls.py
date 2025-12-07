from django.urls import path

from . import views

urlpatterns = [
    path("totp/setup/", views.setup_totp, name="setup_totp"),
    path("totp/verify/", views.verify_totp, name="verify_totp"),
    path("totp/validate/", views.validate_totp, name="validate_totp"),
    path("totp/disable/", views.disable_totp, name="disable_totp"),
    path("webauthn/register/", views.register_webauthn, name="register_webauthn"),
    path("webauthn/list/", views.list_webauthn, name="list_webauthn"),
    path(
        "webauthn/<int:credential_id>/delete/",
        views.delete_webauthn,
        name="delete_webauthn",
    ),
]
