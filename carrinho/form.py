from django import forms

class RemoveProdutoDoCarrinhoForm(forms.Form):
    class Meta:
        fields = ('produto_id')

    produto_id = forms.CharField(widget=forms.HiddenInput())

class EstoqueForm(forms.Form):
    class Meta:
        fields = ('estoque', 'produto_id')

    produto_id = forms.CharField(widget=forms.HiddenInput())

    estoque = forms.IntegerField(
        min_value=1,
        max_value=1000,
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm estoque',
                                      'maxlength': '20',
                                      'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'}),
        required=True)
