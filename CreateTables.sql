create table public.Alunos(
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

create table public.professores(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	registro VARCHAR(10) not null,
	sexo VARCHAR(1) not null,
	data_nascimento date not null,
	data_contratacao date not null,
	flag_ativo boolean default true not null 
)

create table public.disciplinas(
	id SERIAL not null primary key,
	nome VARCHAR(100) not null,
	carga_horaria int not null,
	resumo_disciplina VARCHAR(255),
	id_departamento int
)



