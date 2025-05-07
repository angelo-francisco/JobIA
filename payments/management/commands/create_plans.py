from django.core.management.base import BaseCommand
from payments.models import Plan


class Command(BaseCommand):
    help = "Cria os planos do sistema"

    def handle(self, *args, **options):
        plans = [
            {
                "name": "Essencial",
                "limits": {
                    "max_curriculos": 3,
                    "tipo_curriculo": "básico",
                    "design": "simples",
                    "simulacoes_entrevista": 1,
                    "suporte": "simples",
                    "dicas": True,
                    "preco": 0,
                    "moeda": "Kz",
                },
            },
            {
                "name": "Popular",
                "limits": {
                    "max_curriculos": 10,
                    "tipo_curriculo": "moderno",
                    "design": "elegante",
                    "simulacoes_entrevista": 5,
                    "suporte": "prioritário",
                    "dicas": True,
                    "preco": 2500,
                    "moeda": "Kz",
                    "periodicidade": "mensal",
                },
            },
            {
                "name": "Executivo",
                "limits": {
                    "max_curriculos": "ilimitado",
                    "tipo_curriculo": "premium",
                    "design": "avançado",
                    "simulacoes_entrevista": 12,
                    "suporte": "dedicado",
                    "revisao_manual": True,
                    "carta_apresentacao": True,
                    "preco": 4000,
                    "moeda": "Kz",
                    "periodicidade": "mensal",
                },
            },
            {
                "name": "Elite",
                "limits": {
                    "max_curriculos": "ilimitado",
                    "tipo_curriculo": "premium",
                    "design": "personalizado",
                    "simulacoes_entrevista": "ilimitado",
                    "suporte": "24/7",
                    "revisao_manual": True,
                    "carta_apresentacao": True,
                    "mentoria": "mensal",
                    "grupo_exclusivo": True,
                    "feedback_avancado": True,
                    "personal_branding": True,
                    "preco": 7000,
                    "moeda": "Kz",
                    "periodicidade": "mensal",
                },
            },
        ]

        for plan_data in plans:
            plan, created = Plan.objects.get_or_create(
                name=plan_data["name"], defaults={"limits": plan_data["limits"]}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Plano {plan.name} criado com sucesso!")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️ Plano {plan.name} já existia   "
                    )
                )
