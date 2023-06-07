import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `biblioteca`;")

cursor.execute("CREATE DATABASE `biblioteca`;")

cursor.execute("USE `biblioteca`;")

# criando tabelas
TABLES = {}
TABLES['Livros'] = ('''
      CREATE TABLE `livros` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `categoria` varchar(40) NOT NULL,
      `autor` varchar(50) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Pádua Neto", "PN", generate_password_hash("1234").decode('utf-8')),
      ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
      ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)


cursor.execute('select * from biblioteca.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
livros_sql = 'INSERT INTO livros (nome, categoria, autor) VALUES (%s, %s, %s)'
livros = [
      ('Crepúsculo', 'Romance', 'Stephenie Meyer'),
      ('O Senhor dos Anéis', 'Fantasia', 'J. R. R. Tolkien'),
      ('Harry Potter e a Pedra Filosofal', 'Fantasia', 'J. K. Rowling'),
      ('A Culpa É das Estrelas', 'Romance', 'John Green'),
]
cursor.executemany(livros_sql, livros)

cursor.execute('select * from biblioteca.livros')
print(' -------------  Livros:  -------------')
for livro in cursor.fetchall():
    print(livro[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()