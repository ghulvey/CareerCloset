def user_base_template(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return {'base_template': 'base-admin.html', 'user': request.user}
        return {'base_template': 'base-user.html', 'user': request.user}
    return {'base_template': 'base.html'}