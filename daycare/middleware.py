class HttpsRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if we need to redirect to HTTPS
        if not request.is_secure() and 'HTTP_X_FORWARDED_PROTO' in request.META:
            if request.META['HTTP_X_FORWARDED_PROTO'] == 'https':
                request.is_secure = lambda: True

        response = self.get_response(request)
        return response 