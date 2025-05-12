import requests
from json import loads
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from payments.decorators import user_has_feature_access
from .models import Curriculum
from .utils import get_prompt_for_plan, generate_and_store_pdf
from django.contrib.auth import get_user_model

User = get_user_model()


def home_page(request):
    return render(request, "jobia/home_page.html")


@login_required
@never_cache
def dashboard(request):
    curriculums = Curriculum.objects.filter(
        user=request.user,
        status__in='C'
    )
    return render(request, "jobia/dashboard.html", {'curriculums': curriculums})


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
def generate_curriculum(request, slug):
    try:
        curriculum = Curriculum.objects.get(slug=slug)
    except Curriculum.DoesNotExist:
        return JsonResponse({"error": "Currículo Inexistente"}, status=400)

    if curriculum.status == "C":
        return JsonResponse({"error": "Currículo completo"}, status=400)
    
    if curriculum.user != request.user:
        return JsonResponse({"error": "Esse currículo não é seu"}, status=400)

    try:
        headers = {
            "Authorization": f"Bearer {settings.AI_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": settings.IA_BASE_MESSAGE_CURRICULUM},
                {
                    "role": "user",
                    "content": get_prompt_for_plan(curriculum.user, curriculum.form_data),
                },
            ],
        }

        response = requests.post(
            "https://api.piapi.ai/v1/chat/completions", headers=headers, json=payload
        )

        data = response.json()
        curriculum_html = data['choices'][0]['message']['content']
        curriculum_html = curriculum_html.replace('```html', '').replace('```', '')
        
        generate_and_store_pdf(curriculum, curriculum_html)
        return JsonResponse({'status': 'ok'})
    except Exception as error:
        print(error)
        return JsonResponse({"error": str(error)}, status=500)
    


@login_required
@require_POST
@csrf_exempt
def delete_curriculum(request, slug):
    try:
        curriculum = Curriculum.objects.get(slug=slug)
    except Curriculum.DoesNotExist:
        return JsonResponse({"status": "not_found"}, status=404)

    if request.user == curriculum.user:
        curriculum.delete()
        return JsonResponse({"status": "deletado"})
    return JsonResponse({"error": "Esse currículo não é seu"}, status=400)
