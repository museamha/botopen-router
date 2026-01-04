from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Type your message here...",
            }
        )
    )
