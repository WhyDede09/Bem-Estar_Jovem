from pathlib import Path

from django import forms

from .models import Denuncia

EXTENSOES = {".png", ".jpg", ".jpeg", ".webp", ".pdf"}
MAX_MB = 5


class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ["quem", "tipo", "plataforma", "quando", "descricao", "prova", "risco", "anonima", "nome", "contato"]
        widgets = {
            "quem": forms.RadioSelect,
            "descricao": forms.Textarea(attrs={"rows": 5, "placeholder": "Conte do seu jeito. Não precisa de detalhes que te deixem desconfortável."}),
            "quando": forms.TextInput(attrs={"placeholder": "Ex.: ontem à noite"}),
            "prova": forms.ClearableFileInput(attrs={"accept": ",".join(EXTENSOES)}),
        }

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fields["tipo"].choices = [("", "Escolha…"), *Denuncia.Tipo.choices]
        self.fields["plataforma"].choices = [("", "Escolha…"), *Denuncia.Plataforma.choices]
        for nome, campo in self.fields.items():
            w = campo.widget
            if isinstance(w, (forms.CheckboxInput, forms.RadioSelect)):
                w.attrs["class"] = "form-check-input"
            elif isinstance(w, forms.Select):
                w.attrs["class"] = "form-select"
            else:
                w.attrs["class"] = "form-control"

    def clean_prova(self):
        f = self.cleaned_data.get("prova")
        if not f:
            return f
        if Path(f.name).suffix.lower() not in EXTENSOES:
            raise forms.ValidationError("Envie uma imagem (png, jpg, webp) ou PDF.")
        if f.size > MAX_MB * 1024 * 1024:
            raise forms.ValidationError(f"Arquivo maior que {MAX_MB} MB.")
        return f

    def clean(self):
        d = super().clean()
        if not d.get("anonima") and not d.get("nome"):
            self.add_error("nome", "Para relato identificado, informe seu nome (ou marque anônimo).")
        return d


class RespostaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ["status", "resposta"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "resposta": forms.Textarea(attrs={"class": "form-control", "rows": 4,
                                              "placeholder": "Quem relatou vê esta mensagem ao consultar o protocolo."}),
        }
