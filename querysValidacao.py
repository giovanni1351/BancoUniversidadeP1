"""
Nesse python irei testar as querys que irei usar para validar o banco de dados
Todas as querys devem ser executadas com sucesso e retornar o resultado esperado de 
0 linhas, e sem erros, ou seja, todas as querys devem verificar a existencia de dados
e relações corretas entre as tabelas.

"""
import sqlalchemy
from sqlalchemy import create_engine, inspect, text
import sys

def criar_conexao() -> sqlalchemy.engine.Engine | None:
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        USER = 'postgres.bwvqneansuqchkccmhxq'
        PASSWORD = 'Feisenha123##'
        HOST ='aws-0-sa-east-1.pooler.supabase.com'
        PORT = 5432
        DBNAME = 'postgres'
        SCHEMA = 'public'

        
        DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?options=-csearch_path%3D{SCHEMA}"
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Conexão com o banco de dados estabelecida com sucesso.")
        return engine
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def pegar_informacoes_schema(engine: sqlalchemy.engine.Engine, schema: str = 'public') -> dict:
    """
    Pega informações detalhadas do schema (tabelas, colunas, PKs, FKs).
    """
    inspector = inspect(engine)
    schema_info = {
        'tabelas': {},
        'foreign_keys': []
    }

    try:
        tabelas = inspector.get_table_names(schema=schema)
        for tabela in tabelas:
            colunas = inspector.get_columns(tabela, schema=schema)
            pk_constraint = inspector.get_pk_constraint(tabela, schema=schema)
            primary_keys = pk_constraint['constrained_columns'] if pk_constraint else []

            schema_info['tabelas'][tabela] = {
                'colunas': colunas,
                'primary_keys': primary_keys
            }

            fks = inspector.get_foreign_keys(tabela, schema=schema)
            for fk in fks:
                constrained_columns = fk['constrained_columns'] if isinstance(fk['constrained_columns'], list) else [fk['constrained_columns']]
                referred_columns = fk['referred_columns'] if isinstance(fk['referred_columns'], list) else [fk['referred_columns']]

                if len(constrained_columns) != len(referred_columns):
                     print(f"Aviso: Número de colunas inconsistente na FK da tabela '{tabela}': {fk['name']}")
                     continue
                fk_info = {
                    'referencing_table': tabela,
                    'referencing_columns': constrained_columns,
                    'referred_table': fk['referred_table'],
                    'referred_columns': referred_columns,
                    'name': fk['name']
                }
                schema_info['foreign_keys'].append(fk_info)

    except Exception as e:
        print(f"Erro ao inspecionar o schema '{schema}': {e}")
        return schema_info

    return schema_info


def gerar_querys_validacao(schema_info: dict, schema: str = 'public') -> list[tuple[str, str]]:
    """
    Gera queries SQL para validar nulidade, integridade referencial e participação em N:M.
    Retorna uma lista de tuplas (descricao_da_query, query_sql).
    """
    querys_validacao = []

    # 1. Validar colunas NOT NULL
    for tabela, info_tabela in schema_info.get('tabelas', {}).items():
        for coluna_info in info_tabela.get('colunas', []):
            if not coluna_info['nullable']:
                nome_coluna = coluna_info['name']
                descricao = f"Verifica NULL na coluna {schema}.{tabela}.{nome_coluna} (NOT NULL)"
                query = f'SELECT COUNT(1) FROM "{schema}"."{tabela}" WHERE "{nome_coluna}" IS NULL;'
                querys_validacao.append((descricao, query))

    # 2. Validar integridade referencial (FKs)
    for fk in schema_info.get('foreign_keys', []):
        tabela_origem = fk['referencing_table']
        colunas_origem = fk['referencing_columns']
        tabela_destino = fk['referred_table']
        colunas_destino = fk['referred_columns']
        fk_name = fk['name']

        # Monta as condições do JOIN e do WHERE
        join_conditions = " AND ".join([f't1."{orig}" = t2."{dest}"' for orig, dest in zip(colunas_origem, colunas_destino)])
        where_null_check = " OR ".join([f't2."{dest}" IS NULL' for dest in colunas_destino]) # Se qualquer parte da PK referenciada for nula, o join falha
        # Verifica apenas FKs que não são nulas na origem
        where_origem_not_null = " AND ".join([f't1."{orig}" IS NOT NULL' for orig in colunas_origem])


        descricao = f"Verifica registros órfãos na tabela '{tabela_origem}' pela FK '{fk_name}' para '{tabela_destino}'"
        query = f"""
        SELECT COUNT(1)
        FROM "{schema}"."{tabela_origem}" t1
        LEFT JOIN "{schema}"."{tabela_destino}" t2 ON {join_conditions}
        WHERE ({where_null_check}) AND ({where_origem_not_null});
        """
        querys_validacao.append((descricao, " ".join(query.split())))

    relacoes_nm = [
        ('professores', 'id', 'professor_departamento', 'id_professor'),
        ('departamento', 'id', 'professor_departamento', 'id_departamento'),
        ('professores', 'id', 'professores_disciplinas', 'id_professor'),
        ('disciplinas', 'id', 'professores_disciplinas', 'id_disciplina'),
        ('curso', 'id', 'matriz_curricular', 'id_curso'),
        ('disciplinas', 'id', 'matriz_curricular', 'id_disciplina'),
        ('alunos', 'id', 'aluno_historico_escolar', 'id_aluno'),
        ('historico_escolar', 'id', 'aluno_historico_escolar', 'id_historico_escolar'),
        ('disciplinas', 'id', 'disciplinasalunos', 'id_disciplina'),
        ('alunos', 'id', 'disciplinasalunos', 'id_aluno'),
    ]

    print("\n--- Iniciando validações de participação N:M ---")
    for tabela_principal, pk_principal, tabela_associacao, fk_associacao in relacoes_nm:
        # Verifica se as tabelas existem no schema antes de gerar a query
        if tabela_principal in schema_info.get('tabelas', {}) and tabela_associacao in schema_info.get('tabelas', {}):
            descricao = f"Verifica se todo(a) '{tabela_principal}' possui pelo menos um registro em '{tabela_associacao}'"
            query = f"""
            SELECT COUNT(t1."{pk_principal}")
            FROM "{schema}"."{tabela_principal}" t1
            LEFT JOIN "{schema}"."{tabela_associacao}" t2 ON t1."{pk_principal}" = t2."{fk_associacao}"
            WHERE t2."{fk_associacao}" IS NULL;
            """
            querys_validacao.append((descricao, " ".join(query.split())))
        else:
            print(f"  AVISO: Pulando validação N:M para '{tabela_principal}' <-> '{tabela_associacao}' pois uma ou ambas as tabelas não foram encontradas no schema.")
    print("--- Fim validações N:M ---")

    return querys_validacao

def executar_validacoes(engine: sqlalchemy.engine.Engine, querys: list[tuple[str, str]]) -> bool:
    """
    Executa as queries de validação e reporta falhas.
    Retorna True se todas as validações passaram, False caso contrário.
    """
    todas_passaram = True
    with engine.connect() as connection:
        for descricao, query in querys:
            try:
                print(f"Executando validação: {descricao}")
                result = connection.execute(text(query))
                count = result.scalar_one_or_none()

                if count is None:
                     print(f"  AVISO: A query não retornou um count. Query: {query}")
                elif count > 0:
                    print(f"  FALHA: A validação encontrou {count} linha(s) inválida(s).")
                    print(f"  Query: {query}")
                    todas_passaram = False
                else:
                    print("  SUCESSO: Nenhuma linha inválida encontrada.")

            except Exception as e:
                print(f"  ERRO ao executar a query de validação: {e}")
                print(f"  Query: {query}")
                todas_passaram = False 
            print("-" * 20) 

    return todas_passaram


if __name__ == "__main__":
    schema_banco = 'public'
    engine = criar_conexao()

    if engine:
        print(f"\nInspecionando o schema '{schema_banco}'...")
        schema_info = pegar_informacoes_schema(engine, schema=schema_banco)




        if not schema_info.get('tabelas'):
             print("Nenhuma tabela encontrada no schema ou erro ao buscar informações.")
        else:
            print("\nGerando queries de validação...")
            querys_validacao = gerar_querys_validacao(schema_info, schema=schema_banco)

            if not querys_validacao:
                print("Nenhuma query de validação foi gerada.")
            else:
                print(f"\nIniciando {len(querys_validacao)} validações...")
                resultado_final = executar_validacoes(engine, querys_validacao)

                print("\n--- Resultado Final da Validação ---")
                if resultado_final:
                    print("✅ Todas as validações foram executadas com sucesso e passaram!")
                else:
                    print("❌ Algumas validações falharam ou encontraram erros.")
        engine.dispose()
    else:
        print("Não foi possível conectar ao banco. Saindo.")
        sys.exit(1) 