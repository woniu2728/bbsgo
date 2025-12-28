from django.http import JsonResponse

from core.plugin import runtime


class PluginEnabledMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        runtime.boot_plugins()
        if runtime.is_db_ready():
            path = request.path
            if path.startswith("/api/"):
                response = self._guard_plugin_routes(path)
                if response is not None:
                    return response
        return self.get_response(request)

    def _guard_plugin_routes(self, path: str):
        registry = runtime.get_registry()
        for state in registry.list_states():
            if state.enabled:
                continue
            for mount in state.mounts:
                if path.startswith(f"/api{mount}"):
                    return JsonResponse({"detail": "plugin disabled", "name": state.manifest.name}, status=404)
        return None
