import json
import os

ARQUIVO_USUARIOS = "usuarios.json"


def carregar_usuarios():

    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        return []

    with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_usuarios(lista):

    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)


def usuarioExiste():

    return os.path.exists(ARQUIVO_USUARIOS)


def criarUsuario():

    if not os.path.exists(ARQUIVO_USUARIOS):
        salvar_usuarios([])
        print("Arquivo de usuários criado com sucesso!")


def adicionar_tarefa_usuario(login: str, tarefa_id: int) -> bool:
    """Adiciona uma tarefa ao usuário."""
    usuarios = carregar_usuarios()
    
    for u in usuarios:
        if u["login"] == login:
            if "tarefas" not in u:
                u["tarefas"] = []
            if tarefa_id not in u["tarefas"]:
                u["tarefas"].append(tarefa_id)
            salvar_usuarios(usuarios)
            return True
    
    return False


def cadastrar_usuario(nome, email, login, senha):

    usuarios = carregar_usuarios()

    for u in usuarios:
        if u["login"] == login:
            return False, "Login já existe! Escolha outro."

    novo = {
        "nome": nome,
        "email": email,
        "login": login,
        "senha": senha,
        "tarefas": []
    }

    usuarios.append(novo)
    salvar_usuarios(usuarios)
    return True, "Usuário cadastrado com sucesso!"


def autenticar(login, senha):

    usuarios = carregar_usuarios()

    for u in usuarios:
        if u["login"] == login and u["senha"] == senha:
            return True, u

    return False, None
