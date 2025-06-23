### String

pf = input("Digite seu CPF?")

cpf = cpf.strip()
cpf = cpf.replace('.', '')
cpf = cpf.replace('-', '')

if len(cpf) == 11 and cpf.isnumeric:
    print("CPF incorreto")
else:
    print(cpf)

nome = input("Digite seu nome:")
email = input("Digite seu email?")

if nome and email:
    pos_a = email.find("@")
    servidor = email[pos_a:]
    if pos_a != -1:
        print('cadastro concluído!')
else:
    print('Digite seu nome e email corretamente')

### Listas