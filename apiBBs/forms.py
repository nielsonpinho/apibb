from django import forms


class SolicitaExtrato(forms.Form):


    nome_cliente = forms.CharField(
        label="Nome do cliente",
        max_length=50,
        #min_length=3,
        required=False,
        validators=[],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


    cliente_cpf = forms.CharField(
        label="Numero do CPF ou CNPJ (sem ponto)",
        max_length=14,
        #min_length=3,
        required=False,
        validators=[],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    data_pesquisa = forms.DateField(
        label="Informe a data para Pesquisa",
        required=True,
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={
                'type':"date",
                'class': 'form-control',
                }),
        input_formats=["%d/%m/%Y"]
    )
    