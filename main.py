from time import sleep
import os

# Import seguro de helpers de interface; fornece fallback simples se o pacote não existir

def cabeçalho(titulo: str) -> None:
    print(f"\n=== {titulo} ===")

def menu(opcoes: list) -> int:
    for i, o in enumerate(opcoes, start=1):
        print(f"{i}. {o}")
    while True:
        try:
            escolha = int(input('Escolha: ').strip())
            if 1 <= escolha <= len(opcoes):
                return escolha
        except Exception:
            pass
        print('Opção inválida. Tente novamente.')

from usuario import criarUsuario, usuarioExiste, cadastrar_usuario, autenticar
os.system("cls")
from tarefas import listar_tarefas, cadastrar_tarefa, editar_tarefa, excluir_tarefa, concluir_tarefa, pegar_nome_responsavel
if usuarioExiste():
    print('Arquivo de usuários encontrado.')
else:
    print('Arquivo de usuários não encontrado! Vou criar.')
    criarUsuario()

while True:
    resposta = menu(['LOGIN', 'CADASTRAR', 'TAREFAS',
                    'RELATÓRIOS', 'SAIR DO SISTEMA'])
    if resposta == 1:
        cabeçalho('LOGIN')
        login = input('Login: ').strip()
        senha = input('Senha: ').strip()
        ok, user = autenticar(login, senha)
        if ok:
            print(f"Login realizado com sucesso! Bem-vindo(a), {user.get('nome')}")
        else:
            print('Login falhou: usuário ou senha inválidos.')
    elif resposta == 2:
        cabeçalho('CADASTRAR')
        nome = input('Nome: ').strip()
        email = input('Email: ').strip()
        login = input('Login desejado: ').strip()
        senha = input('Senha: ').strip()
        ok, msg = cadastrar_usuario(nome, email, login, senha)
        print(msg)
    elif resposta == 3:
        # Submenu de tarefas
        while True:
            cabeçalho('TAREFAS')
            opc = menu(['LISTAR', 'CADASTRAR', 'EDITAR', 'EXCLUIR', 'CONCLUIR', 'VOLTAR'])
            if opc == 1:
                cabeçalho('LISTAR TAREFAS')
                tarefas = listar_tarefas()
                if not tarefas:
                    print('Nenhuma tarefa cadastrada.')
                else:
                    for i, t in enumerate(tarefas, start=1):
                        nome_resp = pegar_nome_responsavel(t.responsavel)
                        print(f"{i}. {t.titulo} | {nome_resp} | {t.prazo} | {t.status}\n   {t.descricao}")
            elif opc == 2:
                cabeçalho('CADASTRAR TAREFA')
                titulo = input('Título: ').strip()
                descricao = input('Descrição: ').strip()
                responsavel = input('Responsável: ').strip()
                prazo = input('Prazo (DD/MM/YYYY): ').strip()
                status = input('Status [pendente]: ').strip() or 'pendente'
                try:
                    nova = cadastrar_tarefa(titulo, descricao, responsavel, prazo, status)
                    print('Tarefa cadastrada com sucesso:', nova.titulo)
                except Exception as e:
                    print('Erro ao cadastrar tarefa:', e)
            elif opc == 3:
                cabeçalho('EDITAR TAREFA')
                tarefas = listar_tarefas()
                if not tarefas:
                    print('Nenhuma tarefa para editar.')
                else:
                    for i, t in enumerate(tarefas, start=1):
                        print(f"{i}. {t.titulo} | {t.status}")
                    try:
                        idx = int(input('Número da tarefa: ').strip()) - 1
                        campo = input('Campo para editar (titulo, descricao, responsavel, prazo, status): ').strip()
                        valor = input('Novo valor: ').strip()
                        editada = editar_tarefa(idx, **{campo: valor})
                        print('Tarefa atualizada:', editada.titulo)
                    except Exception as e:
                        print('Erro ao editar tarefa:', e)
            elif opc == 4:
                cabeçalho('EXCLUIR TAREFA')
                tarefas = listar_tarefas()
                if not tarefas:
                    print('Nenhuma tarefa para excluir.')
                else:
                    for i, t in enumerate(tarefas, start=1):
                        print(f"{i}. {t.titulo}")
                    try:
                        idx = int(input('Número da tarefa a excluir: ').strip()) - 1
                        removida = excluir_tarefa(idx)
                        print('Removida:', removida.titulo)
                    except Exception as e:
                        print('Erro ao excluir tarefa:', e)
            elif opc == 5:
                cabeçalho('CONCLUIR TAREFA')
                tarefas = listar_tarefas()
                if not tarefas:
                    print('Nenhuma tarefa para concluir.')
                else:
                    for i, t in enumerate(tarefas, start=1):
                        print(f"{i}. {t.titulo} | {t.status}")
                    try:
                        idx = int(input('Número da tarefa a concluir: ').strip()) - 1
                        concluida = concluir_tarefa(idx)
                        print('Tarefa marcada como concluída:', concluida.titulo)
                    except Exception as e:
                        print('Erro ao concluir tarefa:', e)
            elif opc == 6:
                break
            else:
                print('\033[31mERRO! Digite uma opção válida!\033[m')

            sleep(1)
    elif resposta == 4:
        cabeçalho('RELATÓRIOS 4')
    elif resposta == 5:
        cabeçalho(' Saindo do sistema... Até logo!')
        break
    else:
        print('\033[31mERRO! Digite uma opção válida!\033[m')

    sleep(2)
