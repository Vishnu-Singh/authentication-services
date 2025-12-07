import re

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from auth_core.models import RoutingRule


@api_view(["POST", "GET", "PUT", "DELETE", "PATCH"])
@permission_classes([AllowAny])
def route_request(request):
    """
    Main routing endpoint that forwards authenticated requests to target services.
    Supports REST protocol.
    """
    # Get the target path from query parameter
    target_path = request.GET.get("target")

    if not target_path:
        return Response(
            {"error": "Target path is required as query parameter"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Find matching routing rule
    routing_rule = RoutingRule.objects.filter(
        source_path=target_path, is_active=True
    ).first()

    if not routing_rule:
        return Response(
            {"error": "No routing rule found for this path"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check authentication
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Forward the request to target URL
    try:
        target_url = routing_rule.target_url

        # Prepare headers
        headers = {
            "X-Forwarded-User": request.user.username,
            "X-Forwarded-Email": request.user.email,
            "X-Auth-Method": routing_rule.auth_method,
        }

        # Forward the request
        if request.method == "GET":
            response = requests.get(target_url, headers=headers, params=request.GET)
        elif request.method == "POST":
            response = requests.post(target_url, headers=headers, json=request.data)
        elif request.method == "PUT":
            response = requests.put(target_url, headers=headers, json=request.data)
        elif request.method == "DELETE":
            response = requests.delete(target_url, headers=headers)
        elif request.method == "PATCH":
            response = requests.patch(target_url, headers=headers, json=request.data)

        # Return the response from target service
        return Response(
            (
                response.json()
                if response.headers.get("content-type", "").startswith(
                    "application/json"
                )
                else response.text
            ),
            status=response.status_code,
        )

    except requests.RequestException as e:
        return Response(
            {"error": f"Failed to forward request: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )


@csrf_exempt
def soap_endpoint(request):
    """
    SOAP protocol endpoint for authentication and routing.
    Parses SOAP requests and forwards them to target services.
    """
    if request.method != "POST":
        return HttpResponse(
            '<?xml version="1.0"?><error>Only POST method is supported</error>',
            content_type="text/xml",
            status=405,
        )

    try:
        # Parse SOAP envelope
        soap_body = request.body.decode("utf-8")

        # Extract credentials from SOAP header (simplified)
        username_match = re.search(r"<username>(.*?)</username>", soap_body)
        password_match = re.search(r"<password>(.*?)</password>", soap_body)

        # Extract target service
        target_match = re.search(r"<target>(.*?)</target>", soap_body)

        if not target_match:
            return HttpResponse(
                '<?xml version="1.0"?><error>Target service not specified in SOAP request</error>',
                content_type="text/xml",
                status=400,
            )

        target_service = target_match.group(1)

        # Find routing rule
        routing_rule = RoutingRule.objects.filter(
            source_path=target_service, is_active=True
        ).first()

        if not routing_rule:
            return HttpResponse(
                f'<?xml version="1.0"?><error>No routing rule found for {target_service}</error>',
                content_type="text/xml",
                status=404,
            )

        # Authenticate if credentials provided
        authenticated = False
        if username_match and password_match:
            from django.contrib.auth import authenticate

            user = authenticate(
                username=username_match.group(1), password=password_match.group(1)
            )
            authenticated = user is not None

        if not authenticated:
            return HttpResponse(
                '<?xml version="1.0"?><error>Authentication failed</error>',
                content_type="text/xml",
                status=401,
            )

        # Forward SOAP request to target service
        try:
            response = requests.post(
                routing_rule.target_url,
                data=soap_body,
                headers={"Content-Type": "text/xml"},
            )

            return HttpResponse(
                response.content, content_type="text/xml", status=response.status_code
            )

        except requests.RequestException as e:
            return HttpResponse(
                f'<?xml version="1.0"?><error>Failed to forward SOAP request: {str(e)}</error>',
                content_type="text/xml",
                status=502,
            )

    except Exception as e:
        return HttpResponse(
            f'<?xml version="1.0"?><error>SOAP processing error: {str(e)}</error>',
            content_type="text/xml",
            status=500,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_routes(request):
    """
    List all available routing rules.
    """
    routes = RoutingRule.objects.filter(is_active=True)

    return Response(
        {
            "routes": [
                {
                    "id": route.id,
                    "name": route.name,
                    "source_path": route.source_path,
                    "target_url": route.target_url,
                    "auth_method": route.auth_method,
                    "priority": route.priority,
                }
                for route in routes
            ]
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_route(request):
    """
    Create a new routing rule (admin only).
    """
    if not request.user.is_staff:
        return Response(
            {"error": "Admin privileges required"}, status=status.HTTP_403_FORBIDDEN
        )

    name = request.data.get("name")
    source_path = request.data.get("source_path")
    target_url = request.data.get("target_url")
    auth_method = request.data.get("auth_method", "session")
    priority = request.data.get("priority", 100)

    if not name or not source_path or not target_url:
        return Response(
            {"error": "name, source_path, and target_url are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    route = RoutingRule.objects.create(
        name=name,
        source_path=source_path,
        target_url=target_url,
        auth_method=auth_method,
        priority=priority,
    )

    return Response(
        {
            "message": "Routing rule created successfully",
            "route": {
                "id": route.id,
                "name": route.name,
                "source_path": route.source_path,
                "target_url": route.target_url,
                "auth_method": route.auth_method,
            },
        },
        status=status.HTTP_201_CREATED,
    )
