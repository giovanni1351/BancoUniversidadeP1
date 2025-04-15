
📄 Tabela: professores
  🧱 Coluna: id - Tipo: INTEGER
  🧱 Coluna: nome - Tipo: VARCHAR(100)
  🧱 Coluna: registro - Tipo: VARCHAR(10)
  🧱 Coluna: sexo - Tipo: VARCHAR(1)
  🧱 Coluna: data_nascimento - Tipo: DATE
  🧱 Coluna: data_contratacao - Tipo: DATE
  🧱 Coluna: flag_ativo - Tipo: BOOLEAN
  🔑 Chave Primária: ['id']

📄 Tabela: tcc
  🧱 Coluna: id - Tipo: INTEGER
  🧱 Coluna: id_professor - Tipo: INTEGER
  🧱 Coluna: titulo - Tipo: VARCHAR(255)
  🧱 Coluna: nota - Tipo: DOUBLE PRECISION
  🧱 Coluna: tema - Tipo: VARCHAR(255)
  🔑 Chave Primária: ['id']
  🔗 FK: ['id_professor'] → professores.['id']

📄 Tabela: professores_disciplinas
  🧱 Coluna: id_disciplina - Tipo: INTEGER
  🧱 Coluna: id_professor - Tipo: INTEGER
  🧱 Coluna: semestre - Tipo: INTEGER
  🧱 Coluna: ano - Tipo: INTEGER
  🧱 Coluna: periodo - Tipo: VARCHAR(255)
  🔑 Chave Primária: ['id_disciplina', 'id_professor', 'semestre', 'ano', 'periodo']
  🔗 FK: ['id_disciplina'] → disciplinas.['id']
  🔗 FK: ['id_professor'] → professores.['id']

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

📄 Tabela: curso
  🧱 Coluna: id - Tipo: INTEGER
  🧱 Coluna: id_professor_cordenador - Tipo: INTEGER
  🧱 Coluna: nome - Tipo: VARCHAR(255)
  🧱 Coluna: codigo - Tipo: VARCHAR(255)
  🧱 Coluna: duracao_semestre - Tipo: INTEGER
  🔑 Chave Primária: ['id']
  🔗 FK: ['id_professor_cordenador'] → professores.['id']

📄 Tabela: disciplinas
  🧱 Coluna: id - Tipo: INTEGER
  🧱 Coluna: nome - Tipo: VARCHAR(100)
  🧱 Coluna: carga_horaria - Tipo: INTEGER
  🧱 Coluna: resumo_disciplina - Tipo: VARCHAR(255)
  🧱 Coluna: cod_disciplina - Tipo: VARCHAR(10)
  🧱 Coluna: id_departamento - Tipo: INTEGER
  🔑 Chave Primária: ['id']
  🔗 FK: ['id_departamento'] → departamento.['id']

📄 Tabela: disciplinasalunos
  🧱 Coluna: id_disciplina - Tipo: INTEGER
  🧱 Coluna: id_aluno - Tipo: INTEGER
  🧱 Coluna: ano - Tipo: INTEGER
  🧱 Coluna: semestre_ano - Tipo: INTEGER
  🧱 Coluna: semestre_curso - Tipo: INTEGER
  🔑 Chave Primária: ['id_disciplina', 'id_aluno', 'ano', 'semestre_ano', 'semestre_curso']
  🔗 FK: ['id_aluno'] → alunos.['id']
  🔗 FK: ['id_disciplina'] → disciplinas.['id']

📄 Tabela: aluno_historico_escolar
  🧱 Coluna: id_aluno - Tipo: INTEGER
  🧱 Coluna: id_historico_escolar - Tipo: INTEGER
  🔑 Chave Primária: ['id_aluno', 'id_historico_escolar']
  🔗 FK: ['id_aluno'] → alunos.['id']
  🔗 FK: ['id_historico_escolar'] → historico_escolar.['id']

📄 Tabela: historico_escolar
  🧱 Coluna: id - Tipo: INTEGER
  🧱 Coluna: id_disciplina - Tipo: INTEGER
  🧱 Coluna: nota - Tipo: DOUBLE PRECISION
  🧱 Coluna: status - Tipo: VARCHAR(255)
  🧱 Coluna: data_conclusao - Tipo: DATE
  🧱 Coluna: semestre - Tipo: INTEGER
  🔑 Chave Primária: ['id']
  🔗 FK: ['id_disciplina'] → disciplinas.['id']

📄 Tabela: professor_departamento
  🧱 Coluna: id_professor - Tipo: INTEGER
  🧱 Coluna: id_departamento - Tipo: INTEGER
  🧱 Coluna: is_chefe - Tipo: BOOLEAN
  🔑 Chave Primária: ['id_professor', 'id_departamento']
  🔗 FK: ['id_departamento'] → departamento.['id']
  🔗 FK: ['id_professor'] → professores.['id']

📄 Tabela: departamento
  🧱 Coluna: id - Tipo: INTEGER
  🧱 Coluna: nome - Tipo: VARCHAR(255)
  🧱 Coluna: codigo - Tipo: VARCHAR(10)
  🧱 Coluna: localizacao - Tipo: VARCHAR(255)
  🔑 Chave Primária: ['id']

📄 Tabela: matriz_curricular
  🧱 Coluna: id_curso - Tipo: INTEGER
  🧱 Coluna: id_disciplina - Tipo: INTEGER
  🧱 Coluna: semestre - Tipo: INTEGER
  🔑 Chave Primária: ['id_curso', 'id_disciplina', 'semestre']
  🔗 FK: ['id_curso'] → curso.['id']
  🔗 FK: ['id_disciplina'] → disciplinas.['id']
