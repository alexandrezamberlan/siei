# Sistema de Informação para coleta de indicadores de atletas em esportes de invasão

Sistema Web Python-Django que gerencia registros de indicadores de atletas - SIEI | IFFar Santo Augusto

Este projeto faz parte do Laboratório de Práticas da Computação UFN, em que alunos dos cursos da área de Computação podem praticar o desenvolvimento de sistema Web Python-Django. Além disso, é uma parceria com o professor de Educação Física Fabrício Doring Martins do IFF de Santo Augusto - RS.

O professor Fabrício Doring Martins (fabricio.martins@iffarroupilha.edu.br) foi jogador de voleibol com o Alexandre Zamberlan durante 10 anos.

## Integrantes
    - Fabrício Doring Martins - líder do projeto
    - Alexandre Zamberlan - responsável técnico do projeto
    - Sylvio Vieira - coordenador do Laboratório de Práticas da Computação UFN
    - Camille Rodrigues - Sistemas de Informação
    - Bruno Difante - Ciência da Computação
    - Gabriel Morais - Ciência da Computação
    - Pedro Canabarro - Ciência da Computação

## Estruturação

- apps
    - usuario
        - tipos: administrador, professor, estudante
        - nome
        - sexo
        - dataNascimento
        - peso
        - altura
        - email (chave primária)
        - celular
        - cpf
        - instituição (vinculo com app instituição)
        - is_active
        - slug

        Obs.:
            - usuário faz autocadastro (exceto administrador) - para estudante
                - colocar campo de aceite dos termos de uso
                - verificar se está mandando por email a ativação do usuário
    
    - tipo_instituicao
        - descrição
        - is_active
        - slug

    - instituição
        - nome
        - sigla (opcional)
        - cidade
        - estado
        - país
        - tipo_instituição (vinculo com app tipo_instituicao)
        - is_active
        - slug

    - indicador (fundamento) 
        - descrição                
        - is_active
        - slug
        
    - esporte
        - descrição
        - lista de indicadores (vinculo com app indicador - manytomany)
        - is_active
        - slug
        
    - avaliação
        - estudante (vinculo com app usuario do tipo estudante)
        - esporte (vinculo com app esporte)
        - is_active
        - slug

    - registro_avaliacao
        - avaliacao
        - fundamento
        - resultado
        - is_active
        - slug

    - relatórios
        - a discutir com o professor Fabrício
        

## Sugestões de CSS
    - https://bootswatch.com/3/
    - Icons bootstrap 
        - https://www.w3schools.com/icons/bootstrap_icons_glyphicons.asp

## .env

SECRET_KEY='aoabb!bk-g5s0uk49ecc#%3#3+is(&3+)@ny%3yo0ct0481q43'

DEBUG=True

STATIC_URL=/static/

DOMINIO_URL='localhost:8000'

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_USE_STARTTLS = False

