import os
import json
from pathlib import Path

ARQUIVO_TAREFAS = Path(__file__).with_name("tarefas.json")

def carregar_tarefas():
    try:
        with ARQUIVO_TAREFAS.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, list) and all(isinstance(tarefa, str) for tarefa in dados):
            return dados

        print("O arquivo de tarefas tem um formato inválido. Começando com uma lista vazia.")
    except FileNotFoundError:
        pass  # Na primeira execução, o arquivo ainda não existe.
    except json.JSONDecodeError:
        print("O arquivo de tarefas está inválido. Começando com uma lista vazia.")

    return []

def salvar_tarefas(tarefas):
    try:
        with ARQUIVO_TAREFAS.open("w", encoding="utf-8") as arquivo:
            json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
    except OSError as erro:
        print(f"Não foi possível salvar as tarefas: {erro}")

tarefas = carregar_tarefas()

respostas_aceitas = ['1', '2', '3', '4', '5', 'exit']

tarefa_concluida = False

# FUNÇÃO DE CONFIRMAÇÃO
def confirmar(pergunta):
    while True:
        resposta = input(pergunta).strip().lower()

        if resposta == 's':
            return True
        elif resposta == 'n':
            return False
        else:
            print('Entrada inválida. Digite (s) ou (n).')

# MENU PRINCIPAL
while True:
    os.system('clear')
    print('\n===== GERENCIADOR DE TAREFAS =====')
    print('(1) para adicionar tarefas')
    print('(2) para remover a última tarefa')
    print('(3) para editar a lista')
    print('(4) para mostrar tarefas')
    print('(5) para excluir tarefas')
    print('(exit) para sair')

    input_tarefa = input('\nDigite uma opção: ').strip().lower()

    # SISTEMA DE ENTRADA INVÁLIDA
    if input_tarefa not in respostas_aceitas:
        print('Entrada inválida. Digite uma opção válida.')
        input('Pressione Enter para continuar...')
        continue

    # CONFIRMAÇÃO DE SAÍDA
    if input_tarefa == 'exit':
        if confirmar('Confirmar saída? (s/n): '):
            print('\nPrograma encerrado :)')
            break
        else:
            print('\nVoltando ao menu...')
            input('Pressione Enter para continuar...')
            continue

    # OPÇÃO 1: ADICIONAR TAREFA
    if input_tarefa == '1':
        print('\nDigite suas tarefas. Para voltar ao menu, digite (exit).')

        while True:
            nova_tarefa = input('\nTarefa: ').strip()

            if nova_tarefa.lower() == 'exit':
                print('\nVoltando ao menu...')
                input('Pressione Enter para continuar...')
                break

            if not nova_tarefa:
                print('\nA tarefa não pode ficar vazia.')
                continue

            tarefas.append(nova_tarefa)
            salvar_tarefas(tarefas)
            print(f'Adicionada! Tarefas: ', tarefas)

    # OPÇÃO 2: REMOVER ÚLTIMA TAREFA
    elif input_tarefa == '2':
        if not tarefas:
            print('\nNão há nenhuma tarefa para remover!')
        else:
            print('Suas tarefas:')
            for indice, tarefa in enumerate(tarefas, start=1):
                print(indice, tarefa)
            print(f'\nA tarefa "{tarefas[-1]}" será removida.')

            if confirmar('Deseja remover a última tarefa adicionada? (s/n): '):
                tarefa_removida = tarefas.pop()
                salvar_tarefas(tarefas)
                print(
                    f'Removida: "{tarefa_removida}". '
                    f'Lista atualizada: {tarefas}'
                )
            else:
                print('Remoção cancelada. Voltando ao menu...')

        input('Pressione Enter para continuar...')

    # OPÇÃO 3: EDITAR A LISTA
    elif input_tarefa == '3':
        if not tarefas:
            print('Não há nenhuma tarefa para editar!')
        else:
            print('Suas tarefas:')
            for indice, tarefa in enumerate(tarefas, start=1):
                print(indice, tarefa)

            numero = input('\nNúmero da tarefa que deseja editar: ').strip()

            if not numero.isdigit():
                print('Digite um número válido.')
            else:
                indice = int(numero) - 1

                if not 0 <= indice < len(tarefas):
                    print('Esse número não corresponde a uma tarefa.')
                else:
                    tarefa_editada = input('\nEdite a tarefa: ').strip()

                    if tarefa_editada:
                        tarefas[indice] = tarefa_editada
                        salvar_tarefas(tarefas)
                        print(f'Editado! Lista atualizada: {tarefas}')
                    else:
                        print('A tarefa não pode ficar vazia. Edição cancelada.')

        input('Pressione Enter para continuar...')

    # OPÇÃO 4: MOSTRAR TAREFAS
    elif input_tarefa == '4':
        if not tarefas:
            print('Não há nenhuma tarefa para mostrar!')
        else:
            print('Mostrando suas tarefas:')

            for indice, tarefa in enumerate(tarefas, start=1):
                print(indice, tarefa)

        input('\nPressione Enter para continuar...')

    # OPÇÃO 5: EXCLUIR TODA A LISTA
    elif input_tarefa == '5':
        if not tarefas:
            print('Não há nenhuma tarefa para apagar!')
        else:
            print('Atenção: todas as suas tarefas serão excluídas.')

            if confirmar('Deseja excluir sua lista inteira? (s/n): '):
                tarefas.clear()
                salvar_tarefas(tarefas)
                print('Todas as suas tarefas foram excluídas.')
            else:
                print('Exclusão cancelada. Suas tarefas foram preservadas.')

        input('\nPressione Enter para continuar...')
