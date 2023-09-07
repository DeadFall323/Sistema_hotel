from abc import ABC, abstractmethod

class Garagem(ABC):
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.vagas_disponiveis = list(range(1, capacidade + 1))

    # Função responsavel por remove garagem do cliente, utilizando outro metodo na classe hotel
    def remover_garagem_de_cliente(self, cliente):
        vaga_liberada = cliente.remover_vaga_garagem()
        if vaga_liberada is not None:
            self.vagas_disponiveis.append(vaga_liberada)
            print(f"Vaga de garagem {vaga_liberada} do cliente {cliente.nome_pessoa} liberada.")
        else:
            print("O cliente não possui uma vaga de garagem atribuída.")

    @abstractmethod
    def associar_cliente(self, cliente):
        pass

    @abstractmethod
    def liberar_cliente(self, cliente):
        pass

    # Função responsavel por adicionar uma determinada vaga a lista de disponiveis
    def liberar_vaga(self, numero_vaga):
        if numero_vaga not in self.vagas_disponiveis:
            self.vagas_disponiveis.append(numero_vaga)
class HotelGaragem(Garagem):
    def __init__(self, capacidade, hotel):
        super().__init__(capacidade)
        self.hotel = hotel

    # Função responsavel por linkar cliente a uma vaga de garagem
    def associar_cliente(self, cliente):
        if cliente.precisa_garagem():
            if self.vagas_disponiveis:
                vaga = self.vagas_disponiveis.pop(0)
                cliente.associar_vaga_garagem(vaga)
                print(f"Cliente {cliente.nome_pessoa} associado à vaga de garagem {vaga}.")
            else:
                print("Desculpe, não há mais vagas de garagem disponíveis.")

    # Função responsavel por  exibir vagas disponiveis
    def mostrar_garagens_disponiveis(self):
        print("Vagas de garagem disponíveis:")
        vagas_ocupadas = [cliente.numero_vaga_garagem for cliente in self.hotel.clientes if
                          cliente.numero_vaga_garagem is not None]

        # Cria uma lista com todas as vagas, incluindo as liberadas anteriormente
        todas_as_vagas = list(set(self.vagas_disponiveis + vagas_ocupadas))

        for vaga in todas_as_vagas:
            if vaga in self.vagas_disponiveis:
                print(f"Vaga {vaga}: Disponível")
            else:
                cliente_com_vaga = self.encontrar_cliente_por_vaga(vaga)
                if cliente_com_vaga:
                    print(f"Vaga {vaga}: Quarto {cliente_com_vaga.numero_quarto}")
                else:
                    print(f"Vaga {vaga}: Liberada (anteriormente ocupada)")

        for cliente in self.hotel.clientes:
            if cliente.numero_vaga_garagem is not None and cliente.numero_vaga_garagem not in todas_as_vagas:
                print(
                    f"Cliente {cliente.nome_pessoa} tem uma vaga de garagem, mas não está na lista de vagas disponíveis.")

    # Função responsavel por encontrar o cliente atribuido a vaga
    def encontrar_cliente_por_vaga(self, vaga):
        for cliente in self.hotel.clientes:
            if cliente.numero_vaga_garagem == vaga:
                return cliente
        return None

    # Função responsavel por disponibilizar a vaga de garagem, após a remover vaga desoculpar a vaga
    def liberar_cliente(self, cliente):
        vaga_liberada = cliente.liberar_vaga_garagem()
        if vaga_liberada is not None:
            self.liberar_vaga(vaga_liberada)
            print(f"Vaga de garagem {vaga_liberada} do cliente {cliente.nome_pessoa} liberada.")

    # Função responsavel por atribuir vaga de garagem para um cliente
    def atribuir_garagem_a_cliente(self, cliente):
        if cliente.numero_vaga_garagem is None:
            if self.vagas_disponiveis:
                vaga = self.vagas_disponiveis.pop(0)
                cliente.associar_vaga_garagem(vaga)
                print(f"Cliente {cliente.nome_pessoa} associado à vaga de garagem {vaga}.")
            else:
                print("Desculpe, não há mais vagas de garagem disponíveis.")
        else:
            print("O cliente já possui uma vaga de garagem atribuída.")

    # Função responsavel por remover garagem de cliente, a tornando disponivel
    def remover_garagem_de_cliente(self, cliente):
        vaga_liberada = cliente.remover_vaga_garagem()

        if vaga_liberada is not None:
            self.vagas_disponiveis.append(vaga_liberada)
            print(f"Vaga de garagem {vaga_liberada} do cliente {cliente.nome_pessoa} liberada.")
        else:
            print("O cliente não possui uma vaga de garagem atribuída.")
