# jdbc:postgresql://aws-0-sa-east-1.pooler.supabase.com:5432/postgres?user=postgres.bwvqneansuqchkccmhxq&password=Feisenha123##
from datetime import timedelta
from datetime import datetime, date
from math import floor
import random
import re
from sqlalchemy import create_engine, text, inspect
import pandas as pd
from faker import Faker
import json

import sqlalchemy
config_dados = [
    {
        'function':'generate_data_professores',
        'table':'professores',
        'n': 20,
    },
    {
        'function':'generate_data_departamentos',
        'table':'departamento',
        'n': 10,
    },
    {
        'function':'generate_data_disciplinas',
        'table':'disciplinas',
        'n': 100,
    },
    {
        'function':'generate_data_curso',
        'table':'curso',
        'n': 100,
    },
    {
        'function':'generate_data_tcc',
        'table':'tcc',
        'n': 50,
    },
    {
        'function':'generate_data_alunos',
        'table':'alunos',
        'n': 150,
    },
    {
        'function':'generate_data_matriz_curricular',
        'table':'matriz_curricular',
        'n': 40, # disciplinas por curso no maximo e o minimo é n/2
    },
    {
        'function':'generate_data_professores_disciplinas',
        'table':'professores_disciplinas',
        'n': 100,
    },
    {
        'function':'generate_data_disciplinas_alunos',
        'table':'disciplinasalunos',
        'n': 100,
    },
    {
        'function':'generate_data_historico_escolar',
        'table':'historico_escolar',
        'n': 8*15,
    },
    {
        'function':'generate_data_aluno_historico_escolar',
        'table':'aluno_historico_escolar',
        'n': 100,
    },
    {
        'function':'generate_data_professor_departamento',
        'table':'professor_departamento',
        'n': 3, # Maximo de 3 departamentos por professor
    },   
]
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

def criar_banco():
    """
    Cria o banco de dados
    """
    with open("montaBanco.sql", "r") as arquivo:
        sql = arquivo.read()
    with engine.connect() as conexao:
        conexao.execute(text(sql))
        conexao.commit()
    return True

if criar_banco():
    print("Banco de dados criado com sucesso")
else:
    print("Erro ao criar banco de dados")

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
def generate_data_professores(n):
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
    for i in range(n):
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

def generate_data_departamentos(n):
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
        'Ciência de Dados',
        'Inteligência Artificial',
        'Arquitetura',
        'Design Gráfico',
        'Medicina',
        'Enfermagem',
        'Odontologia',
        'Farmácia',
        'Nutrição',
        'Educação Física',
        'Artes Visuais',
        'Música',
        'Teatro',
        'Cinema',
        'Jornalismo',
        'Publicidade',
        'Relações Internacionais',
        'Ciências Contábeis',
        'Estatística',
        'Astronomia',
        'Geologia',
        'Oceanografia',
        'Meteorologia',
        'Agronomia',
        'Veterinária'
    ]
    lista_departamentos = []
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for nome_departamento in departamentos:
        departamento = {
            'nome': nome_departamento,
            'codigo': random.choice(letras)+random.choice(letras)+str(faker.random_int(min=100, max=999)),
            'localizacao': random.choice(predios),  
        }
        lista_departamentos.append(departamento)

    return lista_departamentos

def generate_data_disciplinas(n):
    """   
        📄 Tabela: disciplinas
        🧱 Coluna: id - Tipo: INTEGER
        🧱 Coluna: nome - Tipo: VARCHAR(100)
        🧱 Coluna: carga_horaria - Tipo: INTEGER
        🧱 Coluna: resumo_disciplina - Tipo: VARCHAR(255)
        🧱 Coluna: id_departamento - Tipo: INTEGER
        🧱 Coluna: cod_disciplina - Tipo: VARCHAR(5)
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
        'Engenharia Biomédica',
        'Engenharia de Biotecnologia',
        'Engenharia de Biofármacos',
        'Cálculo I',
        'Cálculo II',
        'Cálculo III',
        'Álgebra Linear',
        'Estatística',
        'Probabilidade',
        'Programação Orientada a Objetos',
        'Estrutura de Dados',
        'Algoritmos',
        'Banco de Dados',
        'Redes de Computadores',
        'Sistemas Operacionais',
        'Inteligência Artificial',
        'Aprendizado de Máquina',
        'Processamento de Linguagem Natural',
        'Visão Computacional',
        'Robótica',
        'Arquitetura de Computadores',
        'Compiladores',
        'Segurança da Informação',
        'Desenvolvimento Web',
        'Desenvolvimento Mobile',
        'Computação Gráfica',
        'Realidade Virtual',
        'Realidade Aumentada',
        'Computação em Nuvem',
        'Big Data',
        'Internet das Coisas',
        'Blockchain',
        'Criptografia',
        'Ética em Computação',
        'Gestão de Projetos',
        'Empreendedorismo',
        'Contabilidade',
        'Finanças',
        'Marketing Digital',
        'Recursos Humanos',
        'Logística',
        'Gestão da Qualidade',
        'Gestão Ambiental',
        'Sustentabilidade',
        'Anatomia',
        'Fisiologia',
        'Histologia',
        'Embriologia',
        'Genética',
        'Microbiologia',
        'Imunologia',
        'Parasitologia',
        'Farmacologia',
        'Patologia',
        'Bioquímica',
        'Biofísica',
        'Botânica',
        'Zoologia',
        'Ecologia',
        'Geologia',
        'Climatologia',
        'Cartografia',
        'Geopolítica',
        'Antropologia',
        'Arqueologia',
        'Paleontologia',
        'Literatura Brasileira',
        'Literatura Portuguesa',
        'Gramática',
        'Redação',
        'Linguística',
        'Fonética',
        'Semântica',
        'Sintaxe',
        'Morfologia',
        'Pragmática',
        'Tradução',
        'Interpretação de Texto',
        'Lógica',
        'Ética',
        'Metafísica',
        'Epistemologia',
        'Estética',
        'Política',
        'Teoria do Conhecimento',
        'Ciência Política',
        'Relações Internacionais',
        'Direito Constitucional',
        'Direito Civil',
        'Direito Penal',
        'Direito Administrativo',
        'Direito Tributário',
        'Direito Trabalhista',
        'Direito Empresarial',
        'Direito Ambiental',
        'Direito Internacional',
        'Macroeconomia',
        'Microeconomia',
        'Economia Internacional',
        'Economia Monetária',
        'Desenvolvimento Econômico',
        'História Econômica',
        'Física Quântica',
        'Física Nuclear',
        'Termodinâmica',
        'Mecânica Clássica',
        'Eletromagnetismo',
        'Óptica',
        'Acústica',
        'Química Orgânica',
        'Química Inorgânica',
        'Química Analítica',
        'Físico-Química',
        'Química Ambiental'
    ]
    lista_disciplinas = []
    def get_ids_departamentos():
        departamentos = pd.read_sql_query("SELECT id FROM departamento", conexao)
        return departamentos['id'].tolist()
    ids_departamentos = get_ids_departamentos()
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for nome_disciplina in disciplinas:
        disciplina = {
            'nome': nome_disciplina,
            'carga_horaria': faker.random_int(min=10, max=200),
            'resumo_disciplina': faker.text(),
            'id_departamento': random.choice(ids_departamentos),
            'cod_disciplina': random.choice(letras)+random.choice(letras)+str(faker.random_int(min=100, max=999)),
        }
        lista_disciplinas.append(disciplina)

    return lista_disciplinas

def generate_data_curso(n):
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
        'Ciência de Dados',
        'Administração',
        'Direito',
        'Medicina',
        'Enfermagem',
        'Psicologia',
        'Arquitetura e Urbanismo',
        'Design Gráfico',
        'Marketing Digital',
        'Publicidade e Propaganda',
        'Jornalismo',
        'Relações Internacionais',
        'Economia',
        'Contabilidade',
        'Nutrição',
        'Farmácia',
        'Odontologia',
        'Fisioterapia',
        'Educação Física',
        'Pedagogia',
        'Letras - Português',
        'Letras - Inglês',
        'História',
        'Geografia',
        'Filosofia',
        'Sociologia',
        'Música',
        'Artes Visuais',
        'Rede de Computadores',
        'Sistemas Operacionais',
        'Inteligência Artificial',
        'Aprendizado de Máquina',
        'Processamento de Linguagem Natural',
        'Visão Computacional',
        'Robótica'
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

def generate_data_tcc(n):
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
    for i in range(n):
        tcc = {
            'id_professor': random.choice(ids_professores),
            'titulo': faker.sentence(),
            'nota': faker.random_int(min=0, max=10),
            'tema': faker.sentence(),
        }
        lista_tcc.append(tcc)

    return lista_tcc

def generate_data_alunos(n):
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
    
    for i in range(n):
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

def generate_data_matriz_curricular(n):
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
        print(disciplinas)
        return disciplinas['id'].tolist()
    def get_semestres(id_curso:int):
        matriz_curricular = pd.read_sql_query("select c.duracao_semestre from curso c where id = %s", conexao, params=(id_curso,))
        return int(matriz_curricular['duracao_semestre'].iloc[0])
    ids_disciplinas = get_ids_disciplinas()
    for id_curso in ids_cursos:
        quantidade_semestres = get_semestres(id_curso)
        for i in range(n):
            matriz_curricular = {
                'id_curso': id_curso,
                'id_disciplina': random.choice(ids_disciplinas),
                'semestre': faker.random_int(min=1, max=quantidade_semestres),
            }
            lista_matriz_curricular.append(matriz_curricular)

    return lista_matriz_curricular
def generate_data_professores_disciplinas(n):
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
    for i in range(n):
        professores_disciplinas = {
            'id_disciplina': random.choice(ids_disciplinas),
            'id_professor': random.choice(ids_professores),
            'semestre': faker.random_int(min=1, max=8),
            'ano': faker.random_int(min=2020, max=2025),
            'periodo': random.choice(['Matutino', 'Vespertino', 'Noturno']),
        }
        lista_professores_disciplinas.append(professores_disciplinas)

    return lista_professores_disciplinas

def generate_data_disciplinas_alunos(n):
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
    def get_ids_disciplinas(aluno):
        disciplinas = pd.read_sql_query(
            "SELECT id FROM disciplinas WHERE id IN (SELECT id_disciplina FROM matriz_curricular WHERE matriz_curricular.id_curso =  (select a.id_curso  from alunos a where id = %s))", 
            conexao, 
            params=(aluno,)
        )
        return disciplinas['id'].tolist()
    def get_ids_alunos():
        alunos = pd.read_sql_query("SELECT id FROM alunos", conexao)
        return alunos['id'].tolist()
    ids_alunos = get_ids_alunos()
    for id_aluno in ids_alunos:
        ids_disciplinas = get_ids_disciplinas(id_aluno)
        for id_disciplina in ids_disciplinas:
            disciplinas_alunos = {
                'id_disciplina': id_disciplina,
                'id_aluno': id_aluno,
                'ano': faker.random_int(min=2020, max=2025),
                'semestre_ano': faker.random_int(min=1  , max=8),
                'semestre_curso': faker.random_int(min=1, max=8),
            }
            lista_disciplinas_alunos.append(disciplinas_alunos)
    return lista_disciplinas_alunos

def generate_data_historico_escolar(n):
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
    for id_disciplina in ids_disciplinas:
        data_conclusao = faker.date_between(start_date='-2500d', end_date='-1d')
        for semestre in range(1, 8):
            nota = faker.random_int(min=0, max=10)
            if nota >= 5:
                status = 'Aprovado'
            else:
                status = 'Reprovado'
            historico_escolar = {
                'id_disciplina': id_disciplina,
                'nota': nota,
                'status': status,
                'data_conclusao': data_conclusao,   
                'semestre': semestre,
            }
            
            data_conclusao += timedelta(days=30*6)
            lista_historico_escolar.append(historico_escolar)

    return lista_historico_escolar

def generate_data_aluno_historico_escolar(n):
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

    for id in ids_alunos:
        valor_max = faker.random_int(min=1, max=n)
        for i in range(valor_max):
            aluno_historico_escolar = {
                'id_aluno': id,
                'id_historico_escolar': random.choice(ids_historico_escolar),
            }
            lista_aluno_historico_escolar.append(aluno_historico_escolar)

    return lista_aluno_historico_escolar

def generate_data_professor_departamento(n):
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
    
    for id_professor in ids_professores:
        valor_max = faker.random_int(min=1, max=n)
        for i in range(valor_max):
            professor_departamento = {
                'id_professor': id_professor,
                'id_departamento': random.choice(ids_departamentos),
                'is_chefe': faker.boolean()
            }
            lista_professor_departamento.append(professor_departamento)

    return lista_professor_departamento

if truncar_todo_banco(engine):
    print("Tabelas truncadas com sucesso")

for config in config_dados:
    print(f"Iniciando a geração dos dados para a tabela: {config['table']}")
    func = globals()[config['function']]
    data = func(config['n'])
    df = pd.DataFrame(data)
    if config['table'] == 'professor_departamento':
        df = df.drop_duplicates(subset=['id_professor', 'id_departamento'])
    elif config['table'] == 'matriz_curricular':
        df = df.drop_duplicates(subset=['id_curso', 'id_disciplina'])
    elif config['table'] == 'disciplinas':
        df = df.drop_duplicates(subset=['nome'])
    elif config['table'] == 'departamento':
        df = df.drop_duplicates(subset=['nome'])
    else:   
        df = df.drop_duplicates()
    try:
        df.to_sql(config['table'], conexao, if_exists='append', index=False, schema='public')
    except Exception as e:
        print(f"Erro ao gerar dados para a tabela: {config['table']}")
        print(f"Erro: {e}")
        print(f"Dados: {df}")















