from verifica_cpf import validate_cpf

import random
import string
import pickle
import os
import datetime
import time
from garagem import HotelGaragem
from manual import aguarde_com_pontos
from manual import mostrar_manual
from interface import ImplementacaoLogin

class Cliente:
    def __init__(self, nome, idade, cpf, numero):
        self.__nome = nome.title()
        self.__idade = idade
        self.__cpf = cpf
        self.__numero = numero
        self.__quarto = None
        self.__numero_vaga_garagem = None
        self.__vaga_garagem = None

        if validate_cpf(cpf):
            print("CPF válido. Cliente criado.")

        else:
            print("CPF inválido. Criação de cliente cancelada.")
            self.__cpf = None

    def remover_vaga_garagem(self):
        if self.numero_vaga_garagem is not None:
            vaga_liberada = self.numero_vaga_garagem
            self.numero_vaga_garagem = None
            return vaga_liberada
        else:
            return None

    @staticmethod
    def cpf_existente(cpf):
        for cliente in lista_clientes:
            if cliente.cpf_pessoa == cpf:
                return True
        return False
    @property
    def nome_pessoa(self):
        return self.__nome

    @nome_pessoa.setter
    def nome_pessoa(self, novo_nome):
        self.__nome = novo_nome.title()

    @property
    def numero_quarto(self):
        return self.__quarto

    @numero_quarto.setter
    def numero_quarto(self, numero):
        self.__quarto = numero
    @property
    def idade_pessoa(self):
        return self.__idade

    @idade_pessoa.setter
    def idade_pessoa(self, novo_idade):
        self.__idade = novo_idade

    @property
    def numero_vaga_garagem(self):
        return self.__numero_vaga_garagem

    @numero_vaga_garagem.setter
    def numero_vaga_garagem(self, numero):
        self.__numero_vaga_garagem = numero

    @property
    def cpf_pessoa(self):
        return self.__cpf

    @cpf_pessoa.setter
    def cpf_pessoa(self, novo_cpf):
        if validate_cpf(novo_cpf):
            self.__cpf = novo_cpf
        else:
            print("CPF inválido. Operação cancelada.")

    @property
    def numero_pessoa(self):
        return self.__numero

    #Não utilizada
    @numero_pessoa.setter
    def numero_pessoa(self, novo_numero):
        self.__numero = novo_numero

    #Não utilizada
    def cadastrar_cliente(self):
        lista_clientes.append(self)
        print(f"Cliente {self.__nome} cadastrado com sucesso.")

    # Função responsavel por definir o numero do quarto a ser associado ao cliente
    def escolher_quarto(self, numero_quarto):
        self.__quarto = numero_quarto

    # Função responsavel por verificar se o cliente precisa de uma garagem
    def precisa_garagem(self):
        resposta = input("Você precisa de garagem? (S/N): ")
        return resposta.lower() == 's'

    # Função responsavel por linkar uma vaga a um cliente
    def associar_vaga_garagem(self, vaga):
        self.__numero_vaga_garagem = vaga

    # Função responsavel por liberar a vaga para a lista de disponiveis
    def liberar_vaga_garagem(self):
        vaga_liberada = self.numero_vaga_garagem
        self.numero_vaga_garagem = None
        return vaga_liberada

    # Função responsavel por remover a vaga do cliente
    def remover_garagem_de_cliente(self, cliente):
        print(f"Antes de remover a vaga de garagem: {cliente.numero_vaga_garagem}")
        vaga_liberada = cliente.remover_vaga_garagem()
        print(f"Depois de remover a vaga de garagem: {cliente.numero_vaga_garagem}")
        if vaga_liberada is not None:
            self.vagas_disponiveis.append(vaga_liberada)
            print(f"Vaga de garagem {vaga_liberada} do cliente {cliente.nome_pessoa} liberada.")
        else:
            print("O cliente não possui uma vaga de garagem atribuída.")

def salvar_historico(historico):
    with open("historico.pkl", "wb") as file:
        pickle.dump(historico, file)

def carregar_historico():
    try:
        with open("historico.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

class RegistroHistorico:
    def __init__(self, acao, cliente=None):
        self.acao = acao
        self.cliente = cliente
        self.data_hora = datetime.datetime.now()


    def __str__(self):
        if self.cliente:
            return f"{self.data_hora}: {self.acao} - Cliente: {self.cliente.nome_pessoa}"
        else:
            return f"{self.data_hora}: {self.acao}"

class Hotel:
    def __init__(self):
        self.quartos_disponiveis = list(range(1, 61))
        self.clientes = []
        self.garagem = HotelGaragem(30, self)
        self.historico = []
        self.historico = carregar_historico()

    def adicionar_registro_historico(self, acao, cliente=None):
        registro = RegistroHistorico(acao, cliente)
        self.historico.append(registro)

    def mostrar_historico(self):
        print("\nHistórico de Reservas e Baixas:")
        for registro in self.historico:
            print(registro)

    # Função responsavel por mostra os quartos disponiveis, divididos por andar
    def mostrar_quartos_disponiveis(self):
        print("Quartos disponíveis:")
        andares = 6  # Número de andares do prédio
        quartos_por_andar = 10  # Número de quartos por andar

        for andar in range(andares, 0, -1):
            print(f"\nAndar {andar}:")

            for quarto_numero in range(1, quartos_por_andar + 1):
                numero_quarto = (andar - 1) * quartos_por_andar + quarto_numero
                status = "Disponível" if numero_quarto in self.quartos_disponiveis else "Ocupado"
                print(f"Quarto {numero_quarto}: {status}")

    def adicionar_registro_historico(self, acao, cliente=None):
        registro = RegistroHistorico(acao, cliente)
        self.historico.append(registro)
        salvar_historico(self.historico)

    # Função responsavel por verificar se o cpf esta cadastrado atualmente no hotel
    def cpf_existente(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf_pessoa == cpf:
                return True
        return False

    # Função responsavel por efetua busca pelo nome do cliente
    def buscar_cliente_por_nome(self, nome):
        clientes_encontrados = []

        for cliente in self.clientes:
            if cliente.nome_pessoa.lower() == nome.lower():
                clientes_encontrados.append(cliente)

        return clientes_encontrados

    # Função responsavel por cadastrar cliente no hotel
    def cadastrar_novo_cliente(self, nome, idade, cpf, numero):
        if idade >= 18:
            if self.cpf_existente(cpf):
                print("CPF já cadastrado. Não é possível cadastrar o mesmo CPF novamente.")
                return

            if not validate_cpf(cpf):
                print("CPF inválido. Cliente não cadastrado.")
                return

            novo_cliente = Cliente(nome, idade, cpf, numero)
            self.clientes.append(novo_cliente)
            lista_clientes.append(novo_cliente)
            #Historico
            self.adicionar_registro_historico("Cadastro de Cliente", novo_cliente)

            print(f"Novo cliente {nome} cadastrado no hotel.")

            # Exibir lista de quartos disponíveis
            print("Quartos disponíveis:")
            for numero_quarto in range(1, 61):
                if numero_quarto in self.quartos_disponiveis:
                    status = "Disponível"
                else:
                    status = "Ocupado"
                print(f"Quarto {numero_quarto}: {status}")

            # Solicitar ao cliente que escolha um quarto
            numero_quarto = int(input("Escolha o número do quarto: "))
            if numero_quarto in self.quartos_disponiveis:
                if not self.quarto_ocupado(numero_quarto):
                    novo_cliente.escolher_quarto(numero_quarto)
                    self.quartos_disponiveis.remove(numero_quarto)
                    print(f"Cliente {nome} escolheu o quarto {numero_quarto}.")
                    # Associar garagem, se necessário
                    self.garagem.associar_cliente(novo_cliente)
                else:
                    print("Quarto já ocupado.")
            else:
                print("Quarto indisponível ou número inválido.")

        else:
            print("É nescessário ser maior de 18 anos para fazer reserva!")

    # Função responsavel por verificar se o quarto esta ocupado
    def quarto_ocupado(self, numero_quarto):
        for cliente in self.clientes:
            if cliente.numero_quarto == numero_quarto:
                return True
        return False

    # Função responsavel por remover o cliente do cadastro no hotel
    def dar_baixa_cliente(self, cpf_cliente):
        cliente_remover = None
        for cliente in self.clientes:
            if cliente.cpf_pessoa == cpf_cliente:
                cliente_remover = cliente
                break
        if cliente_remover:
            cliente_nome = cliente_remover.nome_pessoa
            quarto_utilizado = cliente_remover.numero_quarto
            vaga_garagem = cliente_remover.numero_vaga_garagem
            #Historico
            self.adicionar_registro_historico("Baixa de Cliente", cliente_remover)

            if quarto_utilizado is not None:
                self.quartos_disponiveis.append(quarto_utilizado)
                cliente_remover.numero_quarto = None
            # Liberar a vaga de garagem, se o cliente tiver uma
            if vaga_garagem is not None:
                self.garagem.liberar_cliente(cliente_remover)
            # Remover o cliente da lista de clientes após liberar a vaga de garagem
            self.clientes.remove(cliente_remover)
            if vaga_garagem is not None:
                print(
                    f"Cliente {cliente_nome} deixou o hotel!\nQuarto utilizado: {quarto_utilizado}\nNúmero da Vaga na Garagem: {vaga_garagem}")
            else:
                print(
                    f"Cliente {cliente_nome} deixou o hotel!\nQuarto utilizado: {quarto_utilizado}\nO cliente não tinha vaga de garagem.")
        else:
            print("Cliente com CPF informado não está cadastrado no hotel.")

    # Função responsavel por mostra os clientes na classe Hotel
    def mostrar_clientes(self):
        print("Clientes cadastrados:")
        for cliente in self.clientes:
            if cliente.numero_quarto is not None:
                quarto = cliente.numero_quarto
                garagem = cliente.numero_vaga_garagem if cliente.numero_vaga_garagem else "Não atribuída"
                print(f"Cliente: {cliente.nome_pessoa}\nQuarto: {quarto}\nVaga de Garagem: {garagem}\n")

    # Função responsavel por carregar os dados armazenados previamente
    def carregar_dados(self):
        try:
            with open("hotel_data.pkl", "rb") as file:
                dados = pickle.load(file)
                self.quartos_disponiveis = dados["quartos_disponiveis"]
                self.clientes = dados["clientes"]
                self.garagem.vagas_disponiveis = dados["vagas_disponiveis"]
        except FileNotFoundError:
            pass

    # Função responsavel por armazenar os dados salvos
    def salvar_dados(self, nome_arquivo="hotel_data.pkl"):
        dados = {
            "quartos_disponiveis": self.quartos_disponiveis,
            "clientes": self.clientes,
            "vagas_disponiveis": self.garagem.vagas_disponiveis
        }
        with open(nome_arquivo, "wb") as file:
            pickle.dump(dados, file)

    # Função responsavel por salvar os dados (NÃO UTILIZADA)
    def salvar_dados_com_data(self):
        data_hora_atual = datetime.datetime.now()
        nome_arquivo = f"hotel_data_{data_hora_atual.strftime('%Y%m%d%H%M%S')}.pkl"
        dados = {
            "quartos_disponiveis": self.quartos_disponiveis,
            "clientes": self.clientes,
            "vagas_disponiveis": self.garagem.vagas_disponiveis
        }
        with open(nome_arquivo, "wb") as file:
            pickle.dump(dados, file)

#Função para mostrar informações do software
def mostrar_informacoes_software():
    nome_do_software = "Sistema de gerenciamento hoteleiro"
    versao_do_software = "Versão 1.2"
    email_de_contato = "kawan.dias@ufpi.edu.br"
    cnpj_do_hotel = "76.032.492/0001-69"
    cep = "64601-297"
    Endereco = "Rua Vital Brasil"
    bairro = "São José"
    cidade = "Picos"
    estado = "Piaui"

    print(22*"-","Sobre",22*"-")
    time.sleep(0.2)
    print("Informações sobre o Software:")
    time.sleep(0.2)
    print(f"Nome do Software: {nome_do_software}")
    time.sleep(0.2)
    print(f"Versão: {versao_do_software}")
    time.sleep(0.2)
    print(f"Email de Contato para Assistência: {email_de_contato}")
    time.sleep(0.2)
    print(f"CNPJ: {cnpj_do_hotel}")
    time.sleep(0.2)
    print(f"CEP: {cep}")
    time.sleep(0.2)
    print(f"Endereço: {Endereco}")
    time.sleep(0.2)
    print(f"Bairro: {bairro}")
    time.sleep(0.2)
    print(f"Cidade: {cidade}")
    time.sleep(0.2)
    print(f"Estado: {estado}")
    print(50 * "-")
    time.sleep(1)

#Função para limpar a tela
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')  # No Windows
    elif 'TERM' in os.environ:
        os.system('clear')  #linux-like e Mac
    else:
        print("Limpeza de tela não suportada neste ambiente.")

#Menu Cliente
def menu_cliente(self):
    while True:
        # limpar_tela()
        print("╔════════════════════════════════════════╗")
        print("║            🌟 Forza Hotel 🌟           ║")
        print("╠════════════════════════════════════════╣")
        print("║  Selecione uma opção:                  ║")
        print("║                                        ║")
        print("║  1 - Mostrar quartos disponiveis       ║")
        print("║  2 - Mostrar garagens disponiveis      ║")
        print("║  0 - Sair                              ║")
        print("╚════════════════════════════════════════╝")
        opcao = input("Insira a opcao ")
        if opcao == '1':
            print("----Mostrar Quartos disponíveis----")
            hotel.mostrar_quartos_disponiveis()
            aguarde_com_pontos()
            time.sleep(2)

        elif opcao == '2':
            print("----Mostrar vagas de garagem disponíveis----")
            hotel.garagem.mostrar_garagens_disponiveis()
            aguarde_com_pontos()
            time.sleep(2)

        elif opcao == '0':
            print("Encerrando o programa.")
            break

        else:
            print("Opção invalida")

#Menu principal do programa
def menu_principal(self):
    while True:
        #limpar_tela()
        print("╔════════════════════════════════════════╗")
        print("║            🌟 Forza Hotel 🌟           ║")
        print("╠════════════════════════════════════════╣")
        print("║  Selecione uma opção:                  ║")
        print("║                                        ║")
        print("║  1 - Cadastrar novo hóspede            ║")
        print("║  2 - Dar baixa em um hóspede           ║")
        print("║  3 - Mostrar clientes cadastrados      ║")
        print("║  4 - Atribuir vaga de garagem a um     ║")
        print("║      cliente                           ║")
        print("║  5 - Remover vaga de garagem de um     ║")
        print("║      cliente                           ║")
        print("║  6 - [DEV] Criar cliente de teste      ║")
        print("║  7 - Buscar cadastro do cliente        ║")
        print("║  8 - Mostrar vagas de garagem          ║")
        print("║  9 - Mostrar quartos disponíveis       ║")
        print("║ 10 - Sobre                             ║")
        print("║ 11 - Mostrar histórico                 ║")
        print("║ 12 - Manual                            ║")
        print("║  0 - Sair                              ║")
        print("║                                        ║")
        print("╚════════════════════════════════════════╝")
        opcao = input("\nDigite o número da opção desejada:")

        if opcao == '1':

            print("------------Cadastrar Cliente------------")
            nome_temp = input("Nome: ")
            idade_temp = int(input("Idade: "))
            cpf_temp = input("CPF: ")
            numero_temp = input("Numero: ")
            hotel.cadastrar_novo_cliente(nome_temp, idade_temp, cpf_temp, numero_temp)
            time.sleep(3)

        elif opcao == '2':
            print("----------Dar baixa no hospede-----------")
            cpf_dar_baixa = input("CPF do cliente para dar baixa: ")
            hotel.dar_baixa_cliente(cpf_dar_baixa)
            aguarde_com_pontos()
            time.sleep(2)

        elif opcao == '3':
            print("-----Mostrar clientes cadastrados--------")
            hotel.mostrar_clientes()
            aguarde_com_pontos()
            #aguarde_com_pontos()
            time.sleep(5)

        elif opcao == '4':
            print("---Atribuir vaga de garagem a cliente----")
            cpf_cliente_atribuir_garagem = input("CPF do cliente para atribuir vaga de garagem: ")
            cliente_atribuir_garagem = None
            for cliente in hotel.clientes:
                if cliente.cpf_pessoa == cpf_cliente_atribuir_garagem:
                    cliente_atribuir_garagem = cliente
                    break
            if cliente_atribuir_garagem:
                hotel.garagem.atribuir_garagem_a_cliente(cliente_atribuir_garagem)
                aguarde_com_pontos()
                time.sleep(2)
            else:
                print("Cliente com CPF informado não está cadastrado no hotel.")
                aguarde_com_pontos()
                time.sleep(2)

        elif opcao == '5':
            print("----Remover vaga de garagem de cliente---")
            cpf_cliente_remover_garagem = input("CPF do cliente para remover vaga de garagem: ")
            cliente_remover_garagem = None
            for cliente in hotel.clientes:
                if cliente.cpf_pessoa == cpf_cliente_remover_garagem:
                    cliente_remover_garagem = cliente
                    break
            if cliente_remover_garagem:
                hotel.garagem.remover_garagem_de_cliente(cliente_remover_garagem)
                print(f"Garagem liberada com sucesso! ")
                aguarde_com_pontos()
            else:
                print("Cliente com CPF informado não está cadastrado no hotel.")
                aguarde_com_pontos()
                time.sleep(2)

        elif opcao == '6':
            print("-----DEV - criar cliente de teste--------")
            generate_test_data(hotel)

        elif opcao == '7':
            print("-----Buscar Cliente por Nome--------")
            nome_busca = input("Digite o nome do cliente: ")
            clientes_encontrados = hotel.buscar_cliente_por_nome(nome_busca)
            if clientes_encontrados:
                print("Clientes encontrados:")
                for cliente in clientes_encontrados:
                    print("Dados do cliente:")
                    print(f"Nome: {cliente.nome_pessoa}")
                    print(f"CPF: {cliente.cpf_pessoa}")
                    print(f"Idade: {cliente.idade_pessoa}")
                    print(f"Número do Quarto: {cliente.numero_quarto}")
                    print(f"Número da Vaga de Garagem: {cliente.numero_vaga_garagem if cliente.numero_vaga_garagem else 'Não atribuída'}")
                    aguarde_com_pontos()
                    time.sleep(2)
            else:
                print("Nenhum cliente encontrado com o nome fornecido.")
                aguarde_com_pontos()
                time.sleep(2)

        elif opcao == '8':
            print("----Mostrar vagas de garagem disponíveis----")
            hotel.garagem.mostrar_garagens_disponiveis()
            aguarde_com_pontos()
            time.sleep(2)

        elif opcao == '9':
            print("----Mostrar Quartos disponíveis----")
            hotel.mostrar_quartos_disponiveis()
            aguarde_com_pontos()
            time.sleep(2)

        elif opcao == '10':
            print("----Mostrar informações de software----")
            mostrar_informacoes_software()
            aguarde_com_pontos()
            time.sleep(3)

        elif opcao == '11':
            print("----Mostrar historico----")
            self.mostrar_historico()
            aguarde_com_pontos()
            time.sleep(4)

        elif opcao == '12':
            print("----Mostrar Manual----")
            mostrar_manual()
            aguarde_com_pontos()
            time.sleep(5)

        elif opcao == '0':
            hotel.salvar_dados()
            print("Encerrando o programa.")
            break

        else:
            print("Opção inválida. Escolha novamente.")
            aguarde_com_pontos()
            time.sleep(2)

'''------------------------função para preencher os dados aleatorios----------------'''

#Função responsavel por pegar letras aleatorias e gerar um nome de exemplo
def generate_random_name():
    letters = string.ascii_letters
    name = ''.join(random.choice(letters) for _ in range(6))
    return name

#Função responsavel por gerar um cpf aleatorio (VALIDO)
def generate_random_cpf():
    cpf_digits = [random.randint(0, 9) for _ in range(9)]

    # Cálculo do primeiro dígito verificador
    total = sum((10 - i) * digit for i, digit in enumerate(cpf_digits))
    remainder = total % 11
    first_digit = (11 - remainder) if remainder > 1 else 0
    cpf_digits.append(first_digit)

    # Cálculo do segundo dígito verificador
    total = sum((11 - i) * digit for i, digit in enumerate(cpf_digits))
    remainder = total % 11
    second_digit = (11 - remainder) if remainder > 1 else 0
    cpf_digits.append(second_digit)

    return ''.join(map(str, cpf_digits))

#Função responsavel por gerar uma idade aleatoria
def generate_random_age():
    return random.randint(18, 99)

#Função responsavel por gerar numero de 8 digitos
def generate_random_number():
    return ''.join(random.choice(string.digits) for _ in range(8))

#Função responsavel por fazer a junção das funções de criação e efetuar o cadastro no hotel
def generate_test_data(hotel):
    random_name = generate_random_name()
    random_cpf = generate_random_cpf()
    random_age = generate_random_age()
    random_number = generate_random_number()

    print(f"Generated data:\nName: {random_name}\nCPF: {random_cpf}\nAge: {random_age}\nNumber: {random_number}")

    hotel.cadastrar_novo_cliente(random_name, random_age, random_cpf, random_number)
    cliente = hotel.clientes[-1]
    print(50*"-")

hotel = Hotel()
garagem = HotelGaragem(30, hotel)
hotel.garagem = garagem
hotel.carregar_dados()
hotel.historico = carregar_historico()
lista_clientes = []

if __name__ == "__main__":
    implementacao = ImplementacaoLogin()

    while True:
        print("------------------------------------------------")
        print("Bem vindo ao sistema de gerenciamento de hotel")
        time.sleep(0.3)
        print("para iniciar, digite seu tipo de usuario")
        time.sleep(0.3)
        print("")
        tipo_usuario = input("Voce é 'cliente' ou 'ADMIN' ?   ")
        print("------------------------------------------------")
        if tipo_usuario not in ["cliente", "ADMIN"]:
            print("Tipo de usuário inválido. Tente novamente.")
            continue

        if tipo_usuario == 'cliente':
            menu_cliente(hotel)
            break

        usuario = 'ADMIN'
        senha = input("Digite a senha(123): ")

        print("------------------------------------------------")

        if implementacao.verificar_login(usuario, senha):
            print(f"Login como {tipo_usuario} bem-sucedido!")

            if tipo_usuario == 'ADMIN':
                menu_principal(hotel)
                break

        else:
            print("Credenciais incorretas. Tente novamente.")

