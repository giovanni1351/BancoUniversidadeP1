 drop table if exists public.Alunos CASCADE
;drop table if exists public.professores CASCADE
;drop table if exists public.disciplinas CASCADE
;drop table if exists public.Professores_Disciplinas CASCADE
;drop table if exists public.DisciplinasAlunos CASCADE
;drop table if exists public.Historico_Escolar CASCADE
;drop table if exists public.Matriz_Curricular CASCADE
;drop table if exists public.Curso CASCADE
;drop table if exists public.Professor_Departamento CASCADE
;drop table if exists public.Departamento CASCADE
;drop table if exists public.Tcc CASCADE
;drop table if exists public.Aluno_Historico_Escolar CASCADE


;create table public.Alunos(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	registro VARCHAR(10) not null,
	sexo varchar(1) not null,
	data_nascimento date not null,
	data_inicio date not null,
	data_fim date,
	id_curso int,
	id_tcc int
)

;create table public.professores(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	registro VARCHAR(10) not null,
	sexo VARCHAR(1) not null,
	data_nascimento date not null,
	data_contratacao date not null,
	flag_ativo boolean default true not null 
)

;create table public.disciplinas(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	carga_horaria int not null,
	resumo_disciplina VARCHAR(255),
	id_departamento int
)

;create table public.Professores_Disciplinas(
	id_disciplina int not null,
	id_professor int not null,
	semestre int not null,
	ano int not null,
	periodo VARCHAR(255) not null,
	primary key (id_disciplina,id_professor,semestre,ano,periodo)
) 


;create table public.DisciplinasAlunos(
	id_disciplina int not null,
	id_aluno int not null,
	ano int not null,
	semestre_ano int not null,
	semestre_curso int not null,
	primary key(id_disciplina,id_aluno,ano,semestre_ano,semestre_curso)
)

;create table public.Historico_Escolar(
	id serial not null primary key 
	,id_disciplina int not null
	,nota float not null
	,status varchar(255) not null
	,data_conclusao date not null
	,semestre int not null 
)

;create table public.Matriz_Curricular(
	id_curso int not null,
	id_disciplina int not null,
	semestre int not null,
	primary key (id_curso,id_disciplina,semestre)
)

;create table public.Curso(
	 id serial not null primary key 
	,id_professor_cordenador int not null
	,nome varchar(255) not null
	,codigo varchar(255) not null
	,duracao_semestre int not null
)
	
;create table public.Professor_Departamento(
	id_professor int not null,
	id_departamento int not null,
	is_chefe boolean,
	primary key(id_professor,id_departamento)
)

;create table public.Departamento(
	id SERIAL not null primary key,
	nome varchar(255) not null,
	codigo varchar(10) not null,
	localizacao varchar(255) not null
)

;create table public.Tcc(
	id serial not null primary key 
	,id_professor int not null
	,titulo varchar(255) not null
	,nota float not null
	,tema varchar(255) not null
)

;create table public.Aluno_Historico_Escolar(
	id_aluno int not null,
	id_historico_escolar int not null,
	primary key(id_aluno,id_historico_escolar)
)
