from django.urls import path

from . import views

urlpatterns = [
    path("metadata/", views.saml_metadata, name="saml_metadata"),
    path("sso/", views.saml_sso, name="saml_sso"),
    path("acs/", views.saml_acs, name="saml_acs"),
    path("slo/", views.saml_slo, name="saml_slo"),
    path("sp/list/", views.saml_sp_list, name="saml_sp_list"),
]
