import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

print("Usuários cadastrados:\n")
cursor.execute("SELECT id, nome, email, cpf, endereco, data_registro FROM usuarios")
usuarios = cursor.fetchall()

for usuario in usuarios:
    print(f"ID: {usuario[0]}")
    print(f"Nome: {usuario[1]}")
    print(f"E-mail: {usuario[2]}")
    print(f"CPF: {usuario[3]}")
    print(f"Endereço: {usuario[4]}")
    print(f"Data de Registro: {usuario[5]}")
    print("-" * 40)

conn.close()
