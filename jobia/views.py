from json import loads

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from payments.decorators import user_has_feature_access
from .models import Curriculum
from django.contrib.auth import get_user_model

User = get_user_model()


def home_page(request):
    return render(request, "jobia/home_page.html")


@login_required
@never_cache
def dashboard(request):
    return render(request, "jobia/dashboard.html")


@login_required
@user_has_feature_access("max_curriculos")
def new_curriculum(request):
    return render(request, "jobia/new_curriculum.html")


@login_required
@user_has_feature_access("max_curriculos")
@require_POST
def get_form_data(request):
    try:
        form_data = loads(request.body)

        user_id = form_data.get("userId", "")

        if not user_id:
            return JsonResponse({"error": "Por favor, tente mais tarde."}, status=400)

        questions = form_data.get("questions", [])

        if not questions:
            return JsonResponse(
                {"error": "Por favor, preencha todos os campos possíveis."}, status=400
            )

        not_answered_questions = 0

        for question in questions:
            if not question["answer"]:
                not_answered_questions += 1

        if not_answered_questions == len(questions):
            return JsonResponse(
                {"error": "Por favor, preencha todos os campos possíveis."}, status=400
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Por favor, tenta mais tarde."}, status=400)

        curriculum = Curriculum.objects.create(user=user, form_data=form_data)

        return JsonResponse({"status": "created", "slug": curriculum.slug})
    except Exception as error:
        return JsonResponse({"error": str(error)}, status=500)


@login_required
@user_has_feature_access("max_curriculos")
def generate_curriculum(request):
    return render(request, "jobia/generate_curriculum.html")
