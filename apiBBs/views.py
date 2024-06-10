from django.shortcuts import render, redirect
from .forms import SolicitaExtrato
from .models import Pesquisa
import requests
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()

appKeyConect = os.getenv('APP_KEY_CONECT')
basicAppKeyConect = os.getenv('BASIC_APP_KEY_CONECT')
url_token = os.getenv('URL_TOKEN')
url_extrato = os.getenv('URL_EXTRATO')
numAgencia = os.getenv('NUM_AGENCIA')
numConta = os.getenv('NUM_CONTA')
certificado = os.getenv('CERTIFICADO')
chave = os.getenv('CHAVE')


@login_required
def index(request):
    """Pagina pricipal"""

    if request.method == "POST":

        return redirect('index')
    
    form = SolicitaExtrato()
    
    
    return render(request, 'apiBBs/index.html',{'form': form} )


@login_required
def pesquisar(request):

    #print(appKeyConect)
    if request.method == "POST":
        form = SolicitaExtrato(request.POST)
       # if form.is_valid():
        cliente_cpf = str(form['cliente_cpf'].value()).replace(" ","")
        nome_cliente = str(form['nome_cliente'].value()).strip().upper()
        data= form["data_pesquisa"].value()
        ano, mes, dia =data.split("-")
        dia = int(dia)
        data_de_pesquisa = str(dia)+mes+ano

       # if request.user.is_authenticated()
        pesquisa_repetida = Pesquisa.objects.filter(text=cliente_cpf+"-"+nome_cliente+"-"+data_de_pesquisa)
        qtd_pesquisa_repetida = len(pesquisa_repetida)
        pesquisa = Pesquisa()
        pesquisa.text = cliente_cpf+"-"+nome_cliente+"-"+data_de_pesquisa
        pesquisa.usuario = request.user.username
        pesquisa.date_added = date.today()
        pesquisa.save()

        extrato = []
        
        token = obterToken(basicAppKeyConect)
        extrato = obterExtrato(token,data_de_pesquisa)
        pesquisa_lancamento = []
        if 'Erro' not in extrato:
            lancamentos = extrato["listaLancamento"]
            if cliente_cpf:
                pesquisa_lancamento = []
                for lancamento in lancamentos:
                    if cliente_cpf in str(lancamento["textoInformacaoComplementar"]).upper() or cliente_cpf in str(lancamento["numeroCpfCnpjContrapartida"]) :
                        if lancamento["textoDescricaoHistorico"] == 'Pix - Recebido':
                            lancamento['horario'] = lancamento['textoInformacaoComplementar'].split()[1]
                            lancamento['cpfCnpjPix'] = lancamento['textoInformacaoComplementar'].split()[2]
                            lancamento['nomeContrapartida'] = ' '.join(lancamento['textoInformacaoComplementar'].split()[3::])
                            data_formatada = str(lancamento['dataLancamento'])
                            if len(str(lancamento['dataLancamento'])) == 7:
                                data_formatada = ('0'+str(lancamento['dataLancamento']))
                            lancamento['dataLancamento'] = data_formatada[:-6:1]+"/"+data_formatada[-6:-4:1]+"/"+data_formatada[-4::1]
                            pesquisa_lancamento.append(lancamento)
                        if lancamento["textoDescricaoHistorico"] == 'Transferência recebida':
                            lancamento['horario'] = lancamento['textoInformacaoComplementar'].split()[1]
                            lancamento['cpfCnpjPix'] = lancamento['numeroCpfCnpjContrapartida']
                            lancamento['nomeContrapartida'] = ' '.join(lancamento['textoInformacaoComplementar'].split()[2::])
                            data_formatada = str(lancamento['dataLancamento'])
                            if len(str(lancamento['dataLancamento'])) == 7:
                                data_formatada = ('0'+str(lancamento['dataLancamento']))
                            lancamento['dataLancamento'] = data_formatada[:-6:1]+"/"+data_formatada[-6:-4:1]+"/"+data_formatada[-4::1]
                            pesquisa_lancamento.append(lancamento)
            if nome_cliente:
                pesquisa_lancamento = []
                for lancamento in lancamentos:
                    if nome_cliente in str(lancamento["textoInformacaoComplementar"]).upper():
                        if lancamento["textoDescricaoHistorico"] == 'Pix - Recebido':
                            lancamento['horario'] = lancamento['textoInformacaoComplementar'].split()[1]
                            lancamento['cpfCnpjPix'] = lancamento['textoInformacaoComplementar'].split()[2]
                            lancamento['nomeContrapartida'] = ' '.join(lancamento['textoInformacaoComplementar'].split()[3::])
                            data_formatada = str(lancamento['dataLancamento'])
                            if len(str(lancamento['dataLancamento'])) == 7:
                                data_formatada = ('0'+str(lancamento['dataLancamento']))
                            lancamento['dataLancamento'] = data_formatada[:-6:1]+"/"+data_formatada[-6:-4:1]+"/"+data_formatada[-4::1]
                            pesquisa_lancamento.append(lancamento)
                        if lancamento["textoDescricaoHistorico"] == 'Transferência recebida':
                            lancamento['horario'] = lancamento['textoInformacaoComplementar'].split()[1]
                            lancamento['cpfCnpjPix'] = lancamento['numeroCpfCnpjContrapartida']
                            lancamento['nomeContrapartida'] = ' '.join(lancamento['textoInformacaoComplementar'].split()[2::])                        
                            data_formatada = str(lancamento['dataLancamento'])
                            if len(str(lancamento['dataLancamento'])) == 7:
                                data_formatada = ('0'+str(lancamento['dataLancamento']))
                            lancamento['dataLancamento'] = data_formatada[:-6:1]+"/"+data_formatada[-6:-4:1]+"/"+data_formatada[-4::1]
                            pesquisa_lancamento.append(lancamento)
                    
            if not pesquisa_lancamento:
                pesquisa_lancamento = 'vazio'

            context = {'extrato': pesquisa_lancamento, 'qtd_pesquisa_repetida': qtd_pesquisa_repetida, 'pesquisas_repetidas':pesquisa_repetida}
           

            return render(request, 'apiBBs/pesquisar.html', context )
        else:
            #print(token + "-- Erro em obter extrato" )
            return render(request, 'apiBBs/index.html' )



def obterToken(basic):

    
    payload = 'grant_type=client_credentials&scope=extrato-info'
    headers = {
        'Authorization': basic,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.request("POST", url_token, headers=headers, data=payload)
        if response.status_code == 200 :
            
            return response.json()["access_token"]
        else:
            return 'Erro na obtencao do token de acesso com erro ' +  str(response.status_code)
    except:
        return 'Erro na fase de obtencao do token'

def obterExtrato(token, data_de_pesquisa):
    url = f"{url_extrato}{numAgencia}/conta/{numConta}?gw-dev-app-key={appKeyConect}&dataInicioSolicitacao={data_de_pesquisa}&dataFimSolicitacao={data_de_pesquisa}"
    payload = {}
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    cert = (f".\{certificado}", f".\{chave}")
            
    try:
        response = requests.get(url, headers=headers, data=payload, cert=cert)
        if response.status_code == 200:
            return response.json()
        else:
            return 'Erro na pesquisa com erro ' + str(response.status_code)
    except:
         return 'Erro na fase de obtencao da pesquisa'
