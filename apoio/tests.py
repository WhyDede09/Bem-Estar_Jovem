from django.test import TestCase

from .models import Denuncia
from .protocolos import novo_protocolo


class ProtocoloTests(TestCase):
    def test_novo_protocolo_tem_formato_esperado(self):
        protocolo = novo_protocolo()

        self.assertRegex(protocolo, r"^ESC-.{4}-.{4}$")


class DenunciaTests(TestCase):
    def criar_denuncia(self, **campos):
        valores = {
            "tipo": "ofensa",
            "plataforma": "whatsapp",
            "descricao": "Relato de teste",
        }
        valores.update(campos)
        return Denuncia.objects.create(**valores)

    def test_save_descarta_identificacao_quando_anonima(self):
        denuncia = self.criar_denuncia(anonima=True, nome="Joana", contato="2º ano")

        self.assertEqual(denuncia.nome, "")
        self.assertEqual(denuncia.contato, "")

    def test_denuncia_e_urgente_se_houver_risco_ou_ameaca(self):
        com_risco = self.criar_denuncia(risco=True)
        ameaca = self.criar_denuncia(tipo="ameaca")
        sem_urgencia = self.criar_denuncia()

        self.assertTrue(com_risco.urgente)
        self.assertTrue(ameaca.urgente)
        self.assertFalse(sem_urgencia.urgente)
