from abc import ABC, abstractmethod


# Defina uma classe abstrata que servirá como sua interface
class InterfaceLogin(ABC):

    @abstractmethod
    def verificar_login(self, usuario, senha):
        pass


# Crie uma classe que implementa a interface
class ImplementacaoLogin(InterfaceLogin):

    def __init__(self):
        self.usuarios = {"cliente": None, "ADMIN": "123"}

    def verificar_login(self, usuario, senha):
        if usuario in self.usuarios and (self.usuarios[usuario] is None or self.usuarios[usuario] == senha):
            return True
        else:
            return False
