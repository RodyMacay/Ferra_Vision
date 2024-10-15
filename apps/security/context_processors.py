

def error_messages(request):
    return {
        'error_messages': request.session.get('error_messages', [])
    }
