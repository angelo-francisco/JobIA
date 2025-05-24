import requests
from json import loads
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings

from payments.decorators import user_has_feature_access
from .models import Curriculum, Interview, InterviewMessage
from .utils import (
    get_prompt_for_plan,
    generate_and_store_pdf,
    get_interview_system_message,
)
from django.contrib.auth import get_user_model

User = get_user_model()


def home_page(request):
    return render(request, "jobia/home_page.html")


@login_required
@never_cache
def dashboard(request):
    curriculums = Curriculum.objects.filter(user=request.user, status__in="C").order_by(
        "-created_at"
    )
    interviews = Interview.objects.filter(user=request.user)
    return render(
        request,
        "jobia/dashboard.html",
        {"curriculums": curriculums, "interviews": interviews},
    )


@login_required
@user_has_feature_access("max_curriculos")
def new_curriculum(request):
    create = request.GET.get("create", False)

    if create == "1" and request.method == "POST":
        title = loads(request.body).get("title", "").strip()

        if not title:
            return JsonResponse(
                {"error": "Preencha o campo para prosseguir, por favor."}, status=400
            )

        curriculum = Curriculum.objects.create(user=request.user, title=title)
        return JsonResponse({"slug": curriculum.slug}, status=201)

    slug = request.GET.get("curriculum", "")

    if not slug:
        return redirect("dashboard")

    curriculum = get_object_or_404(Curriculum, slug=slug, status__in="I")
    return render(request, "jobia/new_curriculum.html")


@login_required
@user_has_feature_access("max_curriculos")
@require_POST
def get_form_data(request, slug):
    curriculum = get_object_or_404(Curriculum, slug=slug)

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

        if request.user != curriculum.user:
            return JsonResponse({"error": "Esse currículo não é seu"}, status=400)
        
        curriculum.form_data = form_data
        curriculum.save()

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
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {"role": "system", "content": settings.IA_BASE_MESSAGE_CURRICULUM},
                {
                    "role": "user",
                    "content": get_prompt_for_plan(
                        curriculum.user, curriculum.form_data
                    ),
                },
            ],
        }

        API_URL = "https://openrouter.ai/api/v1/chat/completions"

        response = requests.post(API_URL, headers=headers, json=payload)

        try:
            data = response.json()
            curriculum_html = data["choices"][0]["message"]["content"]
        except Exception as e:
            return JsonResponse({"error": "Erro ao gerar currículo com IA"}, status=502)

        curriculum_html = curriculum_html.replace("```html", "").replace("```", "")

        generate_and_store_pdf(curriculum, curriculum_html)
        return JsonResponse({"status": "ok", "download_url": curriculum.curriculum})
    except Exception as error:
        print(error)
        return JsonResponse({"error": str(error)}, status=500)


@login_required
@require_POST
def delete_curriculum(request, slug):
    try:
        print(slug)
        curriculum = Curriculum.objects.get(slug=slug)
    except Curriculum.DoesNotExist:
        return JsonResponse({"status": "not_found"}, status=404)

    if request.user == curriculum.user:
        curriculum.delete()
        return JsonResponse({"status": "deletado"})
    return JsonResponse({"error": "Esse currículo não é seu"}, status=400)


@login_required
@require_POST
def delete_interview(request, slug):
    try:
        interview = Interview.objects.get(slug=slug)
    except Interview.DoesNotExist:
        return JsonResponse({"status": "not_found"}, status=404)

    if request.user == interview.user:
        interview.delete()
        return JsonResponse({"status": "deletado"})
    return JsonResponse({"error": "Esta entrevista não foi feita por si"}, status=400)


@login_required
@user_has_feature_access("simulacoes_entrevista")
def interview_start(request):
    if request.method == "POST":
        data = loads(request.body)
        role = data.get("role", "").strip()
        level = data.get("level", "").strip()

        if not role or not level:
            return JsonResponse({"error": "Preencha todos os campos"}, status=400)

        interview = Interview.objects.create(user=request.user, role=role, level=level)

        return JsonResponse({"slug": interview.slug})

    return render(request, "jobia/interview_start.html")


@login_required
def interview_simulation(request, slug):
    interview = get_object_or_404(Interview, slug=slug)
    return render(request, "jobia/interview_simulation.html", {"interview": interview})


@login_required
@require_POST
def get_interview_message(request, slug):
    interview = get_object_or_404(Interview, slug=slug)
    message = loads(request.body).get("message")

    if not message:
        return JsonResponse({"status": "Preencha o campo"}, status=400)

    InterviewMessage.objects.create(interview=interview, sender="U", message=message)

    messages_qs = (
        InterviewMessage.objects.filter(interview=interview)
        .order_by("created_at")
        .values("sender", "message")
    )

    chat_history = []

    chat_history.append({"role": "system", "content": get_interview_system_message()})

    for msg in messages_qs:
        role = "user" if msg["sender"] == "U" else "assistant"
        chat_history.append({"role": role, "content": msg["message"]})

    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": chat_history,
    }

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        interview_message = InterviewMessage.objects.create(
            interview=interview, sender="I", message=reply
        )

        return JsonResponse({"reply": interview_message.message})
    except Exception as e:
        print(e)
        return JsonResponse({"error": f"Erro ao chamar IA: {str(e)}"}, status=500)


@login_required
def get_interview_messages(request, slug):
    interview = get_object_or_404(Interview, slug=slug)

    if interview.user != request.user:
        return JsonResponse({"error": "Não autorizado"}, status=403)

    messages = InterviewMessage.objects.filter(interview=interview).order_by(
        "created_at"
    )

    formatted_messages = [
        {"sender": "user" if msg.sender == "U" else "ai", "text": msg.message}
        for msg in messages
    ]

    return JsonResponse({"messages": formatted_messages})
