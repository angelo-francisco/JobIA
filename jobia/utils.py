from io import BytesIO
from weasyprint import HTML


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


def generate_and_store_pdf(html, file_name):
    pdf_io = BytesIO()    
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)