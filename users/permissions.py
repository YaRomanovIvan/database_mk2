from django.contrib import messages
from django.shortcuts import redirect


def employee_permission(func):
    """
    декоратор на проверку 'роли' пользователя
    """

    def check_permissions(request, *args, **kwargs):
        print(request.user.role)
        if request.user.role == 'USR':
            messages.error(
                request,
                "У вас недостаточно прав!",
            )
            return redirect("index")
        return func(request, *args, **kwargs)

    return check_permissions


def admin_permission(func):
    """
    декоратор на проверку 'роли' пользователя
    """

    def check_permissions(request, *args, **kwargs):
        if request.user.role == 'USR' or request.user.role == 'EMPL':
            messages.error(
                request,
                "У вас недостаточно прав!",
            )
            return redirect("index")
        return func(request, *args, **kwargs)

    return check_permissions