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
        self.fields["tipo"].choices = [("", "Escolha…"), *Denuncia.TIPO_CHOICES]
        self.fields["plataforma"].choices = [("", "Escolha…"), *Denuncia.PLATAFORMA_CHOICES]
        for nome, campo in self.fields.items():
            w = campo.widget  # classes do daisyUI
            w.attrs.setdefault("aria-label", str(campo.label))  # o legend do fieldset não rotula o input
            if nome == "anonima":
                w.attrs["class"] = "toggle toggle-primary"
            elif nome == "risco":
                w.attrs["class"] = "checkbox checkbox-error"
            elif isinstance(w, forms.RadioSelect):
                w.attrs["class"] = "radio radio-primary radio-sm"
            elif isinstance(w, forms.Select):
                w.attrs["class"] = "select w-full"
            elif isinstance(w, forms.Textarea):
                w.attrs["class"] = "textarea w-full"
            elif isinstance(w, forms.ClearableFileInput):
                w.attrs["class"] = "file-input w-full"
            else:
                w.attrs["class"] = "input w-full"

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
            "status": forms.Select(attrs={"class": "select w-full", "aria-label": "Status"}),
            "resposta": forms.Textarea(attrs={"class": "textarea w-full", "rows": 4, "aria-label": "Mensagem para quem relatou",
                                              "placeholder": "Quem relatou vê esta mensagem ao consultar o protocolo."}),
        }
