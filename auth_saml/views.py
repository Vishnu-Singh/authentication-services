from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth_core.models import SAMLServiceProvider


@api_view(["GET"])
@permission_classes([AllowAny])
def saml_metadata(request):
    """
    SAML Identity Provider metadata endpoint.
    Returns the SAML IdP metadata XML.
    """
    base_url = request.build_absolute_uri("/")[:-1]

    metadata_xml = f"""<?xml version="1.0"?>
<EntityDescriptor xmlns="urn:oasis:names:tc:SAML:2.0:metadata"
                  entityID="{base_url}/saml/metadata">
    <IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
        <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                           Location="{base_url}/api/auth/saml/sso/"/>
        <SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                           Location="{base_url}/api/auth/saml/sso/"/>
        <SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                           Location="{base_url}/api/auth/saml/slo/"/>
    </IDPSSODescriptor>
</EntityDescriptor>"""

    return Response(metadata_xml, content_type="application/xml")


@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def saml_sso(request):
    """
    SAML Single Sign-On endpoint.
    Handles SAML authentication requests from Service Providers.
    """
    # In production, parse and validate SAMLRequest
    saml_request = request.POST.get("SAMLRequest") or request.GET.get("SAMLRequest")
    relay_state = request.POST.get("RelayState") or request.GET.get("RelayState")

    if not saml_request:
        return Response(
            {"error": "SAMLRequest parameter is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "message": "SAML SSO request received",
            "note": "In production, this would authenticate the user and return a SAML response",
            "relay_state": relay_state,
            "implementation": "Use python3-saml library for full SAML support",
        }
    )


@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def saml_acs(request):
    """
    SAML Assertion Consumer Service endpoint.
    Receives SAML responses from Identity Providers (when acting as SP).
    """
    saml_response = request.POST.get("SAMLResponse") or request.GET.get("SAMLResponse")
    relay_state = request.POST.get("RelayState") or request.GET.get("RelayState")

    if not saml_response:
        return Response(
            {"error": "SAMLResponse parameter is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "message": "SAML response received",
            "note": "In production, this would validate the SAML response and authenticate the user",
            "relay_state": relay_state,
        }
    )


@api_view(["POST", "GET"])
@permission_classes([AllowAny])
def saml_slo(request):
    """
    SAML Single Logout endpoint.
    Handles SAML logout requests.
    """
    logout_request = request.POST.get("LogoutRequest") or request.GET.get(
        "LogoutRequest"
    )

    if not logout_request:
        return Response(
            {"error": "LogoutRequest parameter is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "message": "SAML logout request received",
            "note": "In production, this would process the logout and return a logout response",
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def saml_sp_list(request):
    """
    List registered SAML Service Providers.
    """
    service_providers = SAMLServiceProvider.objects.filter(is_active=True)

    return Response(
        {
            "service_providers": [
                {
                    "entity_id": sp.entity_id,
                    "acs_url": sp.acs_url,
                    "slo_url": sp.slo_url,
                    "created_at": sp.created_at,
                }
                for sp in service_providers
            ]
        }
    )
