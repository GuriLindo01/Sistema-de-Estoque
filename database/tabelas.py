from database.conexao import conectar

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT, 
            categoria TEXT,
            quantidade INTEGER NOT NULL DEFAULT 0,
            preco_compra REAL NOT NULL,
            preco_venda REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Ativo' 
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL, 
            quantidade INTEGER NOT NULL,
            desconto REAL DEFAULT 0.0,
            data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    ''')
    
    conexao.commit()
    conexao.close()
    print("Banco de dados funcionando")