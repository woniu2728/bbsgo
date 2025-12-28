from django.http import HttpResponse


class SimpleCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_origins = {
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        }

    def __call__(self, request):
        origin = request.headers.get("Origin")
        if request.method == "OPTIONS":
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        if origin in self.allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
            response["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
        return response
