from io import BytesIO
from weasyprint import HTML
from cloudinary.uploader import upload


def get_prompt_for_plan(user, raw_data):
    plan = user.subscription.plan.name
    design = "simples"

    if plan == "Profissional":
        design = "Elegante"
    elif plan == "Executivo":
        design = "Um pouco mais elegante que o profissional"
    elif plan == "Elite":
        design = "Moderno"

    return f"""Gere um currículo para o plano {plan}, com design {design}, com os seguintes dados: {raw_data}"""


def generate_and_store_pdf(curriculum, html):
    pdf_io = BytesIO()    
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    upload_result = upload(
        pdf_io,
        resource_type="raw",
        public_id=f"{curriculum.slug}.pdf"
    )
    
    print(upload_result)
    curriculum.curriculum = upload_result['secure_url']
    curriculum.status = 'C'
    curriculum.save()


def get_interview_system_role(role, level):
    return f"""Você é um entrevistador experiente.Simule uma entrevista real para o cargo de {role} no nível {level}.Inicie com uma saudação formal, e conduza uma série de perguntas técnicas e comportamentais.Não responda pelo usuário. Espere a resposta e só depois prossiga."""