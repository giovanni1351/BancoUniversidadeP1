import random
from sqlalchemy import create_engine, text, inspect
import pandas as pd
from faker import Faker
import json

def criar_conexao():

    # Fetch variables
    USER = 'postgres.bwvqneansuqchkccmhxq'
    PASSWORD = 'Feisenha123##'
    HOST ='aws-0-sa-east-1.pooler.supabase.com'
    PORT =5432
    DBNAME = 'postgres'

    # Construct the SQLAlchemy connection string
    DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
    engine = create_engine(DATABASE_URL)
    return engine

engine = criar_conexao()

def pegar_schema(engine):
    """
    Pega o schema do banco de dados utilizando o SQLAlchemy inspector
    """
        # Instanciando o inspetor
    inspector = inspect(engine)

    # Lista todas as tabelas
    tabelas = inspector.get_table_names(schema='public')

    for tabela in tabelas:
        print(f"\n📄 Tabela: {tabela}")
        
        # Colunas
        colunas = inspector.get_columns(tabela, schema='public')
        for col in colunas:
            print(f"  🧱 Coluna: {col['name']} - Tipo: {col['type']}")

        # Chave primária
        pk = inspector.get_pk_constraint(tabela, schema='public')
        print(f"  🔑 Chave Primária: {pk.get('constrained_columns', [])}")

        # Chaves estrangeiras
        fks = inspector.get_foreign_keys(tabela, schema='public')
        for fk in fks:
            print(f"  🔗 FK: {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")

        

# schema = pegar_schema(engine)
faker = Faker('pt_BR') 

conexao = criar_conexao()
def generate_data_professores():
    """ Tabela: professores
        🧱 Coluna: id - Tipo: INTEGER
        🧱 Coluna: nome - Tipo: VARCHAR(100)
        🧱 Coluna: registro - Tipo: VARCHAR(10)
        🧱 Coluna: sexo - Tipo: VARCHAR(1)
        🧱 Coluna: data_nascimento - Tipo: DATE
        🧱 Coluna: data_contratacao - Tipo: DATE
        🧱 Coluna: flag_ativo - Tipo: BOOLEAN
        🔑 Chave Primária: ['id']
    """
    lista_professores = []
    for i in range(10):
        professor = {
            'nome': faker.name(),
            'registro': faker.random_int(min=1000000000, max=9999999999),
            'sexo': faker.random_element(elements=('M', 'F')),
            'data_nascimento': faker.date_of_birth(),
            'data_contratacao': faker.date_between(start_date='-30d', end_date='today'),
            'flag_ativo': faker.boolean(),
        }
        lista_professores.append(professor)

    return lista_professores

def generate_data_departamentos():
    """
        📄 Tabela: departamento
        🧱 Coluna: id - Tipo: INTEGER
        🧱 Coluna: nome - Tipo: VARCHAR(255)
        🧱 Coluna: codigo - Tipo: VARCHAR(10)
        🧱 Coluna: localizacao - Tipo: VARCHAR(255)
        🔑 Chave Primária: ['id']
    """
    predios = [
        'Predio 1',
        'Predio 2',
        'Predio 3',
        'Predio 4',
        'Predio 5',
        'Predio 6',
        'Predio 7'
    ]
    departamentos = [
        'Matemática',
        'Engenharia',
        'Computação',
        'Física',
        'Química',
        'Biologia',
        'Geografia',
        'História',
        'Português',
        'Inglês',
        'Espanhol',
        'Filosofia',
        'Sociologia',
        'Psicologia',
        'Direito',
        'Economia',
        'Administração',
        'Marketing',
        'Engenharia de Software',
        'Engenharia de Computação',
        'Engenharia de Telecomunicações',
        'Engenharia de Automação',
        'Engenharia de Bioprocessos',
        'Engenharia de Biomateriais',
        'Engenharia de Biomédica',
        'Engenharia de Biotecnologia',
        'Engenharia de Biofármacos',
        'Engenharia de Bioprocessos',
        'Engenharia de Biomateriais',
        'Engenharia de Biomédica',
        'Engenharia de Biotecnologia',
        'Engenharia de Biofármacos',
        'Engenharia de Bioprocessos',
        'Engenharia de Biomateriais',
        'Engenharia de Biomédica',
        'Engenharia de Biotecnologia',
        'Engenharia de Biofármacos'
    ]
    lista_departamentos = []
    for i in range(10):
        departamento = {
            'nome': random.choice(departamentos),
            'codigo': faker.random_int(min=1000000000, max=9999999999),
            'localizacao': random.choice(predios),  
        }
        lista_departamentos.append(departamento)

    return lista_departamentos

def generate_data_disciplinas():
    """   
        📄 Tabela: disciplinas
        🧱 Coluna: id - Tipo: INTEGER
        🧱 Coluna: nome - Tipo: VARCHAR(100)
        🧱 Coluna: carga_horaria - Tipo: INTEGER
        🧱 Coluna: resumo_disciplina - Tipo: VARCHAR(255)
        🧱 Coluna: id_departamento - Tipo: INTEGER
        🔑 Chave Primária: ['id']
        🔗 FK: ['id_departamento'] → departamento.['id']
     """
    disciplinas = [
        'Matemática',
        'Engenharia',
        'Computação',
        'Física',
        'Química',
        'Biologia',
        'Geografia',
        'História',
        'Português',
        'Inglês',
        'Espanhol',
        'Filosofia',
        'Sociologia',
        'Psicologia',
        'Direito',
        'Economia',
        'Administração',
        'Marketing',
        'Engenharia de Software',
        'Engenharia de Computação',
        'Engenharia de Telecomunicações',
        'Engenharia de Automação',
        'Engenharia de Bioprocessos',
        'Engenharia de Biomateriais',
        'Engenharia de Biomédica',
        'Engenharia de Biotecnologia',
        'Engenharia de Biofármacos',
        'Engenharia de Bioprocessos',
        'Engenharia de Biomateriais',
        'Engenharia de Biomédica',
        'Engenharia de Biotecnologia',
        'Engenharia de Biofármacos'
    ]
    lista_disciplinas = []
    def get_ids_departamentos():
        departamentos = pd.read_sql_query("SELECT id FROM departamento", conexao)
        return departamentos['id'].tolist()
    ids_departamentos = get_ids_departamentos()
    for i in range(10):
        disciplina = {
            'nome': random.choice(disciplinas),
            'carga_horaria': faker.random_int(min=10, max=200),
            'resumo_disciplina': faker.text(),
            'id_departamento': random.choice(ids_departamentos),
        }
        lista_disciplinas.append(disciplina)

    return lista_disciplinas

def generate_data_curso():
    """
        📄 Tabela: curso
        🧱 Coluna: id - Tipo: INTEGER
        🧱 Coluna: nome - Tipo: VARCHAR(255)
        🧱 Coluna: codigo - Tipo: VARCHAR(255)
        🧱 Coluna: duracao_semestre - Tipo: INTEGER
        🔑 Chave Primária: ['id']
    """
    nomes_cursos = [
        'Engenharia de Software',
        'Engenharia de Computação',
        'Engenharia de Telecomunicações',
        'Engenharia de Automação',
        'Engenharia de Bioprocessos',
        'Engenharia de Biomateriais',
        'Engenharia de Biomédica',
        'Engenharia de Biotecnologia',
        'Engenharia de Biofármacos',
        'Engenharia de Bioprocessos',
        'Engenharia de Biomateriais',
        'Ciência da Computação',
        'Ciência de Dados'
    ]
    lista_curso = []
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for nome_curso in nomes_cursos:
        curso = {
            'nome': nome_curso,
            'codigo': random.choice(letras)+random.choice(letras)+str(faker.random_int(min=1, max=100)),
            'duracao_semestre': faker.random_int(min=4, max=12),
        }
        lista_curso.append(curso)

    return lista_curso


# professores = generate_data_professores()
# professores_df = pd.DataFrame(professores)
# professores_df.to_sql('professores', conexao, if_exists='append', index=False, schema='public')

# departamentos = generate_data_departamentos()
# departamentos_df = pd.DataFrame(departamentos)
# departamentos_df.to_sql('departamento', conexao, if_exists='append', index=False, schema='public')

# disciplinas = generate_data_disciplinas()
# disciplinas_df = pd.DataFrame(disciplinas)
# disciplinas_df.to_sql('disciplinas', conexao, if_exists='append', index=False, schema='public')

curso = generate_data_curso()
curso_df = pd.DataFrame(curso)
curso_df.to_sql('curso', conexao, if_exists='append', index=False, schema='public')














