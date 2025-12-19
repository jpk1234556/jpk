from django.http import JsonResponse
from django.db import connection
from django.utils import timezone


def health(request):
    db_ok = True
    db_error = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as e:
        db_ok = False
        db_error = str(e)

    data = {
        "status": "ok" if db_ok else "degraded",
        "timestamp": timezone.now().isoformat(),
        "checks": {
            "database": {
                "ok": db_ok,
                "error": db_error,
            }
        }
    }
    status_code = 200 if db_ok else 503
    return JsonResponse(data, status=status_code)
