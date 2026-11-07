from django.contrib.auth import get_user_model
from django.test import TestCase


class EntrarSairTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user("coord", password="senha123", is_staff=True)
        User.objects.create_user("comum", password="senha123")

    def test_coordenacao_entra_e_vai_para_o_painel(self):
        resposta = self.client.post("/coordenacao/entrar/", {"username": "coord", "password": "senha123"})

        self.assertRedirects(resposta, "/coordenacao/")

    def test_senha_errada_mostra_erro(self):
        resposta = self.client.post("/coordenacao/entrar/", {"username": "coord", "password": "errada"})

        self.assertContains(resposta, "Usuário ou senha incorretos")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_usuario_sem_is_staff_nao_entra(self):
        resposta = self.client.post("/coordenacao/entrar/", {"username": "comum", "password": "senha123"})

        self.assertContains(resposta, "Usuário ou senha incorretos")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_next_para_outro_site_e_ignorado(self):
        resposta = self.client.post("/coordenacao/entrar/",
                                    {"username": "coord", "password": "senha123", "next": "https://site-malicioso.com"})

        self.assertRedirects(resposta, "/coordenacao/")

    def test_sair_so_por_post(self):
        self.client.login(username="coord", password="senha123")

        self.assertEqual(self.client.get("/coordenacao/sair/").status_code, 405)
        resposta = self.client.post("/coordenacao/sair/")
        self.assertRedirects(resposta, "/coordenacao/entrar/")
        self.assertNotIn("_auth_user_id", self.client.session)
