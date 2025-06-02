nome = input("Qual é o seu nome?")
altura = float(input("Qual é a sua altura?"))
peso = float(input( "Qual é o seu peso?"))

imc = peso/(altura**2)

print("Olá {}! com a altura {}m e o peso {}kg, seu IMC é {}." .format(nome, altura, peso, imc)) #com format
#print(f"Olá {nome}! com a altura {altura}m e o peso {peso}kg, seu IMC é {imc}.") #com f-string

if 25 < imc < 29.9:
    print("Sobrepeso")
elif 18.5 < imc < 24.9:
    print("Peso normal")
elif imc < 18.5:
    print("Abaixo do peso normal")    
else:
    print("Obesidade")