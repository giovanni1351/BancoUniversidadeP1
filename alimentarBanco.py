# jdbc:postgresql://aws-0-sa-east-1.pooler.supabase.com:5432/postgres?user=postgres.bwvqneansuqchkccmhxq&password=Feisenha123##

import random
import re
from sqlalchemy import create_engine, text, inspect
import pandas as pd
from faker import Faker
import json

import sqlalchemy

def criar_conexao()->sqlalchemy.engine.Engine:

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
    schema = ""
        # Instanciando o inspetor
    inspector = inspect(engine)

    # Lista todas as tabelas
    tabelas = inspector.get_table_names(schema='public')

    for tabela in tabelas:
        schema+= f"\n📄 Tabela: {tabela}\n"
        # print(f"\n📄 Tabela: {tabela}")
        
        # Colunas
        colunas = inspector.get_columns(tabela, schema='public')
        for col in colunas:
            schema+=f"  🧱 Coluna: {col['name']} - Tipo: {col['type']}\n"
            # print(f"  🧱 Coluna: {col['name']} - Tipo: {col['type']}")

        # Chave primária
        pk = inspector.get_pk_constraint(tabela, schema='public')
        schema +=f"  🔑 Chave Primária: {pk.get('constrained_columns', [])}\n"
        # print(f"  🔑 Chave Primária: {pk.get('constrained_columns', [])}")

        # Chaves estrangeiras
        fks = inspector.get_foreign_keys(tabela, schema='public')
        for fk in fks:
            schema +=f"  🔗 FK: {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}\n"
            # print(f"  🔗 FK: {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")

    return schema

def truncar_todo_banco(engine:sqlalchemy.engine.Engine):
    """
    Trunca todas as tabelas do banco de dados
    """
    inspector = inspect(engine)
    tabelas = inspector.get_table_names(schema='public')
    for tabela in tabelas:
        with engine.connect() as conexao:
            conexao.execute(text(f"TRUNCATE TABLE {tabela} RESTART IDENTITY CASCADE"))
            conexao.commit()
        print(f"Tabela {tabela} truncada com sucesso")
    return True

schema = pegar_schema(engine)
print(schema)
with open('Schema.md', 'w', encoding='utf-8') as arquivo:
    arquivo.write(schema)
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
        🧱 Coluna: id_professor_cordenador - Tipo: INTEGER
        🔑 Chave Primária: ['id']
        🔗 FK: ['id_professor_cordenador'] → professores.['id']
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
    def get_ids_professores():
        professores = pd.read_sql_query("SELECT id FROM professores", conexao)
        return professores['id'].tolist()
    ids_professores = get_ids_professores()
    for nome_curso in nomes_cursos:
        curso = {
            'nome': nome_curso,
            'codigo': random.choice(letras)+random.choice(letras)+str(faker.random_int(min=1, max=100)),
            'duracao_semestre': faker.random_int(min=4, max=12),
            'id_professor_cordenador': random.choice(ids_professores),
        }
        lista_curso.append(curso)

    return lista_curso

def generate_data_tcc():
    """
    📄 Tabela: tcc
    🧱 Coluna: id - Tipo: INTEGER
    🧱 Coluna: id_professor - Tipo: INTEGER
    🧱 Coluna: titulo - Tipo: VARCHAR(255)
    🧱 Coluna: nota - Tipo: DOUBLE PRECISION
    🧱 Coluna: tema - Tipo: VARCHAR(255)
    🔑 Chave Primária: ['id']
    🔗 FK: ['id_professor'] → professores.['id']
    """
    lista_tcc = []
    def get_ids_professores():
        professores = pd.read_sql_query("SELECT id FROM professores", conexao)
        return professores['id'].tolist()
    ids_professores = get_ids_professores()
    for i in range(10):
        tcc = {
            'id_professor': random.choice(ids_professores),
            'titulo': faker.sentence(),
            'nota': faker.random_int(min=0, max=10),
            'tema': faker.sentence(),
        }
        lista_tcc.append(tcc)

    return lista_tcc

def generate_data_alunos():
    """
        📄 Tabela: alunos
        🧱 Coluna: id - Tipo: INTEGER
        🧱 Coluna: nome - Tipo: VARCHAR(100)
        🧱 Coluna: registro - Tipo: VARCHAR(10)
        🧱 Coluna: sexo - Tipo: VARCHAR(1)
        🧱 Coluna: data_nascimento - Tipo: DATE
        🧱 Coluna: data_inicio - Tipo: DATE
        🧱 Coluna: data_fim - Tipo: DATE
        🧱 Coluna: id_curso - Tipo: INTEGER
        🧱 Coluna: id_tcc - Tipo: INTEGER
        🔑 Chave Primária: ['id']
        🔗 FK: ['id_curso'] → curso.['id']
        🔗 FK: ['id_tcc'] → tcc.['id']
    """
    lista_alunos = []
    def get_ids_cursos():
        cursos = pd.read_sql_query("SELECT id FROM curso", conexao)
        return cursos['id'].tolist()
    ids_cursos = get_ids_cursos()
    def get_ids_tcc():
        tcc = pd.read_sql_query("SELECT id FROM tcc", conexao)
        return tcc['id'].tolist()
    ids_tcc = get_ids_tcc()
    sexos = ['M', 'F']
    
    for i in range(10):
        aluno = {
            'nome': faker.name(),
            'registro': faker.random_int(min=1000000000, max=9999999999),
            'sexo': random.choice(sexos),
            'data_nascimento': faker.date_of_birth(),
            'data_inicio': faker.date_between(start_date='-30d', end_date='today'),
            'data_fim': faker.date_between(start_date='-30d', end_date='today'),
            'id_curso': random.choice(ids_cursos),
            'id_tcc': random.choice(ids_tcc),
        }
        lista_alunos.append(aluno)

    return lista_alunos

def generate_data_matriz_curricular():
    """
    📄 Tabela: matriz_curricular
    🧱 Coluna: id_curso - Tipo: INTEGER
    🧱 Coluna: id_disciplina - Tipo: INTEGER
    🧱 Coluna: semestre - Tipo: INTEGER
    🔑 Chave Primária: ['id_curso', 'id_disciplina', 'semestre']
    🔗 FK: ['id_curso'] → curso.['id']
    🔗 FK: ['id_disciplina'] → disciplinas.['id']
    """
    lista_matriz_curricular = []
    def get_ids_cursos():
        cursos = pd.read_sql_query("SELECT id FROM curso", conexao)
        return cursos['id'].tolist()
    ids_cursos = get_ids_cursos()
    def get_ids_disciplinas():
        disciplinas = pd.read_sql_query("SELECT id FROM disciplinas", conexao)
        return disciplinas['id'].tolist()
    ids_disciplinas = get_ids_disciplinas()
    for i in range(10):
        matriz_curricular = {
            'id_curso': random.choice(ids_cursos),
            'id_disciplina': random.choice(ids_disciplinas),
            'semestre': faker.random_int(min=1, max=8),
        }
        lista_matriz_curricular.append(matriz_curricular)

    return lista_matriz_curricular
def generate_data_professores_disciplinas():
    """
    📄 Tabela: professores_disciplinas
    🧱 Coluna: id_disciplina - Tipo: INTEGER
    🧱 Coluna: id_professor - Tipo: INTEGER
    🧱 Coluna: semestre - Tipo: INTEGER
    🧱 Coluna: ano - Tipo: INTEGER
    🧱 Coluna: periodo - Tipo: VARCHAR(255)
    🔑 Chave Primária: ['id_disciplina', 'id_professor', 'semestre', 'ano', 'periodo']
    🔗 FK: ['id_disciplina'] → disciplinas.['id']
    🔗 FK: ['id_professor'] → professores.['id']
    """
    lista_professores_disciplinas = []
    def get_ids_disciplinas():
        disciplinas = pd.read_sql_query("SELECT id FROM disciplinas", conexao)
        return disciplinas['id'].tolist()
    ids_disciplinas = get_ids_disciplinas()
    def  get_ids_professores():
        professores = pd.read_sql_query("SELECT id FROM professores", conexao)
        return professores['id'].tolist()
    ids_professores = get_ids_professores()
    for i in range(10):
        professores_disciplinas = {
            'id_disciplina': random.choice(ids_disciplinas),
            'id_professor': random.choice(ids_professores),
            'semestre': faker.random_int(min=1, max=8),
            'ano': faker.random_int(min=2020, max=2025),
            'periodo': random.choice(['Matutino', 'Vespertino', 'Noturno']),
        }
        lista_professores_disciplinas.append(professores_disciplinas)

    return lista_professores_disciplinas

def generate_data_disciplinas_alunos():
    """
    📄 Tabela: disciplinasalunos
    🧱 Coluna: id_disciplina - Tipo: INTEGER
    🧱 Coluna: id_aluno - Tipo: INTEGER
    🧱 Coluna: ano - Tipo: INTEGER
    🧱 Coluna: semestre_ano - Tipo: INTEGER
    🧱 Coluna: semestre_curso - Tipo: INTEGER
    🔑 Chave Primária: ['id_disciplina', 'id_aluno', 'ano', 'semestre_ano', 'semestre_curso']
    🔗 FK: ['id_aluno'] → alunos.['id']
    🔗 FK: ['id_disciplina'] → disciplinas.['id']
    """
    lista_disciplinas_alunos = []
    def get_ids_disciplinas():
        disciplinas = pd.read_sql_query("SELECT id FROM disciplinas", conexao)
        return disciplinas['id'].tolist()
    ids_disciplinas = get_ids_disciplinas()
    def get_ids_alunos():
        alunos = pd.read_sql_query("SELECT id FROM alunos", conexao)
        return alunos['id'].tolist()
    ids_alunos = get_ids_alunos()
    for i in range(10):
        disciplinas_alunos = {
            'id_disciplina': random.choice(ids_disciplinas),
            'id_aluno': random.choice(ids_alunos),
            'ano': faker.random_int(min=2020, max=2025),
            'semestre_ano': faker.random_int(min=1, max=8),
            'semestre_curso': faker.random_int(min=1, max=8),
        }
        lista_disciplinas_alunos.append(disciplinas_alunos)
    return lista_disciplinas_alunos

def generate_data_historico_escolar():
    """
    📄 Tabela: historico_escolar
    🧱 Coluna: id - Tipo: INTEGER
    🧱 Coluna: id_disciplina - Tipo: INTEGER
    🧱 Coluna: nota - Tipo: DOUBLE PRECISION
    🧱 Coluna: status - Tipo: VARCHAR(255)
    🧱 Coluna: data_conclusao - Tipo: DATE
    🧱 Coluna: semestre - Tipo: INTEGER
    🔑 Chave Primária: ['id']
    🔗 FK: ['id_disciplina'] → disciplinas.['id']
    """
    lista_historico_escolar = []
    def get_ids_disciplinas():
        disciplinas = pd.read_sql_query("SELECT id FROM disciplinas", conexao)
        return disciplinas['id'].tolist()
    ids_disciplinas = get_ids_disciplinas()
    for i in range(10):
        nota = faker.random_int(min=0, max=10)
        if nota >= 5:
            status = 'Aprovado'
        else:
            status = 'Reprovado'
        historico_escolar = {
            'id_disciplina': random.choice(ids_disciplinas),
            'nota': nota,
            'status': status,
            'data_conclusao': faker.date_between(start_date='-30d', end_date='today'),
            'semestre': faker.random_int(min=1, max=8),
        }
        lista_historico_escolar.append(historico_escolar)

    return lista_historico_escolar

def generate_data_aluno_historico_escolar():
    """
    📄 Tabela: aluno_historico_escolar
    🧱 Coluna: id_aluno - Tipo: INTEGER
    🧱 Coluna: id_historico_escolar - Tipo: INTEGER
    🔑 Chave Primária: ['id_aluno', 'id_historico_escolar']
    🔗 FK: ['id_aluno'] → alunos.['id']
    🔗 FK: ['id_historico_escolar'] → historico_escolar.['id']
    """
    lista_aluno_historico_escolar = []
    def get_ids_alunos():
        alunos = pd.read_sql_query("SELECT id FROM alunos", conexao)
        return alunos['id'].tolist()
    ids_alunos = get_ids_alunos()
    def get_ids_historico_escolar():
        historico_escolar = pd.read_sql_query("SELECT id FROM historico_escolar", conexao)
        return historico_escolar['id'].tolist()
    ids_historico_escolar = get_ids_historico_escolar()
    for i in range(10):
        aluno_historico_escolar = {
            'id_aluno': random.choice(ids_alunos),
            'id_historico_escolar': random.choice(ids_historico_escolar),
        }
        lista_aluno_historico_escolar.append(aluno_historico_escolar)

    return lista_aluno_historico_escolar

def generate_data_professor_departamento():
    """
    📄 Tabela: professor_departamento
    🧱 Coluna: id_professor - Tipo: INTEGER
    🧱 Coluna: id_departamento - Tipo: INTEGER
    🧱 Coluna: is_chefe - Tipo: BOOLEAN
    🔑 Chave Primária: ['id_professor', 'id_departamento']
    🔗 FK: ['id_departamento'] → departamento.['id']
    🔗 FK: ['id_professor'] → professores.['id']
    """
    lista_professor_departamento = []
    def get_ids_professores():
        professores = pd.read_sql_query("SELECT id FROM professores", conexao)
        return professores['id'].tolist()
    ids_professores = get_ids_professores()
    def get_ids_departamentos():
        departamentos = pd.read_sql_query("SELECT id FROM departamento", conexao)
        return departamentos['id'].tolist()
    ids_departamentos = get_ids_departamentos()
    for i in range(10):
        professor_departamento = {
            'id_professor': random.choice(ids_professores),
            'id_departamento': random.choice(ids_departamentos),
            'is_chefe': faker.boolean()
        }
        lista_professor_departamento.append(professor_departamento)

    return lista_professor_departamento

if truncar_todo_banco(engine):
    print("Tabelas truncadas com sucesso")

professores = generate_data_professores()
professores_df = pd.DataFrame(professores)
professores_df.to_sql('professores', conexao, if_exists='append', index=False, schema='public')

departamentos = generate_data_departamentos()
departamentos_df = pd.DataFrame(departamentos)
departamentos_df.to_sql('departamento', conexao, if_exists='append', index=False, schema='public')

disciplinas = generate_data_disciplinas()
disciplinas_df = pd.DataFrame(disciplinas)
disciplinas_df.to_sql('disciplinas', conexao, if_exists='append', index=False, schema='public')

curso = generate_data_curso()
curso_df = pd.DataFrame(curso)
curso_df.to_sql('curso', conexao, if_exists='append', index=False, schema='public')

tcc = generate_data_tcc()
tcc_df = pd.DataFrame(tcc)
tcc_df.to_sql('tcc', conexao, if_exists='append', index=False, schema='public')

alunos = generate_data_alunos()
alunos_df = pd.DataFrame(alunos)
alunos_df.to_sql('alunos', conexao, if_exists='append', index=False, schema='public')

matriz_curricular = generate_data_matriz_curricular()
matriz_curricular_df = pd.DataFrame(matriz_curricular)
matriz_curricular_df = matriz_curricular_df.drop_duplicates()
matriz_curricular_df.to_sql('matriz_curricular', conexao, if_exists='append', index=False, schema='public')

professores_disciplinas = generate_data_professores_disciplinas()
professores_disciplinas_df = pd.DataFrame(professores_disciplinas)
professores_disciplinas_df = professores_disciplinas_df.drop_duplicates()
professores_disciplinas_df.to_sql('professores_disciplinas', conexao, if_exists='append', index=False, schema='public')

disciplinas_alunos = generate_data_disciplinas_alunos()
disciplinas_alunos_df = pd.DataFrame(disciplinas_alunos)
disciplinas_alunos_df = disciplinas_alunos_df.drop_duplicates()
disciplinas_alunos_df.to_sql('disciplinasalunos', conexao, if_exists='append', index=False, schema='public')

historico_escolar = generate_data_historico_escolar()
historico_escolar_df = pd.DataFrame(historico_escolar)
historico_escolar_df.to_sql('historico_escolar', conexao, if_exists='append', index=False, schema='public')

aluno_historico_escolar = generate_data_aluno_historico_escolar()
aluno_historico_escolar_df = pd.DataFrame(aluno_historico_escolar)
aluno_historico_escolar_df = aluno_historico_escolar_df.drop_duplicates()
aluno_historico_escolar_df.to_sql('aluno_historico_escolar', conexao, if_exists='append', index=False, schema='public')

professor_departamento = generate_data_professor_departamento()
professor_departamento_df = pd.DataFrame(professor_departamento)
professor_departamento_df = professor_departamento_df.drop_duplicates()
professor_departamento_df.to_sql('professor_departamento', conexao, if_exists='append', index=False, schema='public')


















