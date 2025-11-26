import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any

from persistencia import salvar_tarefas, carregar_tarefas
from usuario import carregar_usuarios, adicionar_tarefa_usuario

ALLOWED_STATUS = {"pendente", "em progresso", "concluída"}


@dataclass
class Tarefa:
    titulo: str
    descricao: str
    responsavel: str
    prazo: str  # DD/MM/YYYY
    status: str = "pendente"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Tarefa":
        return Tarefa(
            titulo=d.get("titulo", ""),
            descricao=d.get("descricao", ""),
            responsavel=d.get("responsavel", ""),
            prazo=d.get("prazo", ""),
            status=d.get("status", "pendente"),
        )


def validar_prazo(prazo: str) -> bool:
    try:
        datetime.strptime(prazo, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_status(status: str) -> bool:
    return status in ALLOWED_STATUS


def validar_responsavel(login: str) -> bool:
    usuarios = carregar_usuarios()
    return any(u.get("login") == login for u in usuarios)


def pegar_nome_responsavel(login: str) -> str:
    usuarios = carregar_usuarios()
    u = next((x for x in usuarios if x.get("login") == login), None)
    if u:
        return u.get("nome", login)
    return login


def obter_tarefas() -> List[Tarefa]:
    data = carregar_tarefas()
    return [Tarefa.from_dict(d) for d in data]


def persistir_tarefas(tarefas: List[Tarefa]) -> None:
    salvar_tarefas([t.to_dict() for t in tarefas])


def cadastrar_tarefa(titulo: str, descricao: str, responsavel: str, prazo: str, status: str = "pendente") -> Tarefa:
    if not validar_prazo(prazo):
        raise ValueError("Prazo inválido. Use o formato DD/MM/YYYY.")
    if not validar_status(status):
        raise ValueError(f"Status inválido. Use um entre: {', '.join(ALLOWED_STATUS)}")
    if not validar_responsavel(responsavel):
        raise ValueError("Responsável inválido: login não encontrado.")

    tarefas = obter_tarefas()
    nova = Tarefa(titulo=titulo, descricao=descricao, responsavel=responsavel, prazo=prazo, status=status)
    tarefas.append(nova)
    
    # Obter o índice da tarefa recém-adicionada
    tarefa_id = len(tarefas) - 1
    
    # Vincular a tarefa ao usuário
    if not adicionar_tarefa_usuario(responsavel, tarefa_id):
        raise ValueError("Não foi possível vincular a tarefa ao usuário.")
    
    persistir_tarefas(tarefas)
    return nova


def listar_tarefas() -> List[Tarefa]:
    return obter_tarefas()


def editar_tarefa(indice: int, **campos) -> Tarefa:
    tarefas = obter_tarefas()
    if not (0 <= indice < len(tarefas)):
        raise IndexError("Índice de tarefa inválido.")

    tarefa = tarefas[indice]
    if "prazo" in campos and not validar_prazo(campos["prazo"]):
        raise ValueError("Prazo inválido. Use o formato DD/MM/YYYY.")
    if "status" in campos and not validar_status(campos["status"]):
        raise ValueError(f"Status inválido. Use um entre: {', '.join(ALLOWED_STATUS)}")
    if "responsavel" in campos and not validar_responsavel(campos["responsavel"]):
        raise ValueError("Responsável inválido: login não encontrado.")

    for k, v in campos.items():
        if hasattr(tarefa, k):
            setattr(tarefa, k, v)

    persistir_tarefas(tarefas)
    return tarefa


def excluir_tarefa(indice: int) -> Tarefa:
    tarefas = obter_tarefas()
    if not (0 <= indice < len(tarefas)):
        raise IndexError("Índice de tarefa inválido.")
    removida = tarefas.pop(indice)
    persistir_tarefas(tarefas)
    return removida


def concluir_tarefa(indice: int) -> Tarefa:
    return editar_tarefa(indice, status="concluída")


if __name__ == "__main__":
    os.system("cls")
    # Pequena interface interativa para uso rápido
    while True:
        print("\n--- Gerenciador de Tarefas ---")
        print("1) Listar tarefas")
        print("2) Cadastrar tarefa")
        print("3) Editar tarefa")
        print("4) Excluir tarefa")
        print("5) Concluir tarefa")
        print("0) Sair")
        escolha = input("Escolha uma opção: ")
        try:
            if escolha == "1":
                tarefas = listar_tarefas()
                if not tarefas:
                    print("Nenhuma tarefa cadastrada.")
                else:
                    for i, t in enumerate(tarefas, start=1):
                                nome_resp = pegar_nome_responsavel(t.responsavel)
                                print(f"{i}. {t.titulo} | {nome_resp} | {t.prazo} | {t.status}\n   {t.descricao}")
            elif escolha == "2":
                titulo = input("Título: ")
                descricao = input("Descrição: ")
                responsavel = input("Responsável: ")
                prazo = input("Prazo (DD/MM/YYYY): ")
                status = input(f"Status ({'/'.join(ALLOWED_STATUS)}) [pendente]: ") or "pendente"
                nova = cadastrar_tarefa(titulo, descricao, responsavel, prazo, status)
                print("Tarefa cadastrada:", nova)
            elif escolha == "3":
                tarefas = listar_tarefas()
                for i, t in enumerate(tarefas, start=1):
                    print(f"{i}. {t.titulo} | {t.status}")
                idx = int(input("Número da tarefa: ")) - 1
                campo = input("Campo para editar (titulo, descricao, responsavel, prazo, status): ")
                valor = input("Novo valor: ")
                editada = editar_tarefa(idx, **{campo: valor})
                print("Tarefa atualizada:", editada)
            elif escolha == "4":
                tarefas = listar_tarefas()
                for i, t in enumerate(tarefas, start=1):
                    print(f"{i}. {t.titulo}")
                idx = int(input("Número da tarefa a excluir: ")) - 1
                removida = excluir_tarefa(idx)
                print("Removida:", removida.titulo)
            elif escolha == "5":
                tarefas = listar_tarefas()
                for i, t in enumerate(tarefas, start=1):
                    print(f"{i}. {t.titulo} | {t.status}")
                idx = int(input("Número da tarefa a concluir: ")) - 1
                concluida = concluir_tarefa(idx)
                print("Tarefa marcada como concluída:", concluida.titulo)
            elif escolha == "0":
                break
            else:
                print("Opção inválida.")
        except Exception as e:
            print("Erro:", e)