from flask import Response

def success(message):
    return Response(message, status=200)
