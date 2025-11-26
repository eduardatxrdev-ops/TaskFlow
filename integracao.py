from usuario import criarUsuario, usuarioExiste, cadastrar_usuario, carregar_usuarios
from tarefas import cadastrar_tarefa, listar_tarefas
import os

# Garantir que o arquivo de usuários exista
if not usuarioExiste():
    criarUsuario()

# Definir um usuário de integração
login = "teste_integ"
nome = "Usuário Integração"
email = "integ@example.com"
senha = "senha123"

# Verificar se usuário já existe
usuarios = carregar_usuarios()
user = next((u for u in usuarios if u.get("login") == login), None)
if not user:
    ok, msg = cadastrar_usuario(nome, email, login, senha)
    if not ok:
        print("Falha ao cadastrar usuário:", msg)
    else:
        print("Usuário criado:", login)
else:
    print("Usuário já existe:", login)

# Cadastrar uma tarefa para esse usuário
try:
    tarefa = cadastrar_tarefa(
        titulo=f"Tarefa de {login}",
        descricao="Tarefa criada pelo script de integração",
        responsavel=login,
        prazo="31/12/2025"
    )
    print("Tarefa cadastrada:", tarefa.titulo)
except Exception as e:
    print("Erro ao cadastrar tarefa:", e)

# Listar tarefas atribuídas ao usuário
all_tarefas = listar_tarefas()
minhas = [t for t in all_tarefas if t.responsavel == login]

print("\n== Relatório de Integração ==")
print(f"Usuário: {login} - Nome: {nome} - Email: {email}")
print(f"Total de tarefas no sistema: {len(all_tarefas)}")
print(f"Tarefas atribuídas a {login}: {len(minhas)}")
for i, t in enumerate(minhas, start=1):
    print(f"{i}. {t.titulo} | {t.prazo} | {t.status}\n   {t.descricao}")
