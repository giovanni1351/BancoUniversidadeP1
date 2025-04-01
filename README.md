# Tabelas
- Alunos 
- Professores 
- Disciplinas 
- Curso
- Departamento 
- Tcc 
- Historico_Escolar 
- Prof_Depart 
- Professores_Disciplinas
- Matriz_Curricular 
- Aluno_Historico_Escolar
- DisciplinasAlunos 
## Diagrama
```mermaid
erDiagram
    DisciplinasAlunos }| -- || Alunos: Possui
    Alunos }|--|| Curso : Cadastrado_em
    Professores_Disciplinas }| -- || Disciplinas : Lecionado_Por
    Professores_Disciplinas }| -- || Professores : Leciona
    DisciplinasAlunos }| -- || Disciplinas: Possui

    Tcc }o--|| Professores: Possui
    Tcc ||--|{ Alunos: Possui
    Historico_Escolar }| -- || Disciplinas : Possui
    Prof_Depart }| -- || Professores : Possui
    Prof_Depart }| -- || Departamento : Possui
    Departamento ||--|{ Disciplinas: Possui
    Matriz_Curricular }| -- || Disciplinas: Possui
    Aluno_Historico_Escolar}| -- || Alunos : Possui
    Matriz_Curricular }| -- || Curso: Possui
    Aluno_Historico_Escolar}| -- || Historico_Escolar : Possui

    Alunos {
        int id PK
        string nome
        string registro
        string sexo
        date data_nascimento
        date data_inicio
        date data_fim
        int id_curso FK
        int id_tcc FK
    }
    
    Professores {
        int id PK
        string nome 
        string registro
        string sexo
        date data_nascimento
        date data_contratacao
    }
    
    Disciplinas {
        int id PK
        string codigo
        string nome
        int carga_horaria
        string ementa
        int id_departamento FK
    }
    
    Curso {
        int id PK
        string nome
        string codigo
        int duracao_semestres
    }
    
    Departamento {
        int id PK
        string nome
        string codigo
        string localizacao
    }
    
    Tcc {
        int id PK
        string titulo
        date data_entrega
        float nota
        string tema
        int id_professor FK
    }
    
    Historico_Escolar {
        int id PK
        int id_disciplina FK
        float nota
        string status
        date data_conclusao
        int semestre
    }   
    Prof_Depart {
        int id_professor PK
        int id_professor FK
        int id_departamento PK
        int id_departamento FK

    }
    Professores_Disciplinas {
        int id_disciplina PK
        int id_disciplina FK
        int id_professor PK
        int id_professor FK
        int semestre PK
        int ano PK
        string periodo PK
    }

    Matriz_Curricular {
        int id_curso PK
        int id_disciplina PK
        int semestre PK
    }
    Aluno_Historico_Escolar{
        int id_Aluno PK
        int id_Aluno FK
        int id_Historico_Escolar PK
        int id_Historico_Escolar FK


    }
    DisciplinasAlunos {
        int id_disciplina PK
        int id_aluno PK
        int ano PK
        int semestre_ano PK
        int semestre_curso PK
        string periodo PK

    }
```
--- 
## Alunos 
- int id PK
- string nome
- string registro
- string sexo
- date data_nascimento
- date data_inicio
- date data_fim
- int id_curso FK
- int id_tcc FK


## Professores 
- int id PK
- string nome 
- string registro
- string sexo
- date data_nascimento
- date data_contratacao


## Disciplinas 
- int id PK
- string codigo
- string nome
- int carga_horaria
- string ementa
- int id_departamento FK


## Curso 
- int id PK
- string nome
- string codigo
- int duracao_semestres

## Departamento 
- int id PK
- string nome
- string codigo
- string localizacao


## Tcc 
- int id PK
- string titulo
- date data_entrega
- float nota
- string tema
- int id_professor FK


## Historico_Escolar 
- int id PK
- int id_disciplina FK
- float nota
- string status
- date data_conclusao
- int semestre

## Prof_Depart 
- int id_professor PK
- int id_professor FK
- int id_departamento PK
- int id_departamento FK


## Professores_Disciplinas 
- int id_disciplina PK
- int id_professor PK
- int semestre PK
- int ano PK
- string periodo PK


## Matriz_Curricular 
- int id_curso PK
- int id_disciplina PK
- int semestre PK

## Aluno_Historico_Escolar
- int id_Aluno PK
- int id_Aluno FK
- int id_Historico_Escolar PK
- int id_Historico_Escolar FK


## DisciplinasAlunos 
- int id_disciplina PK
- int id_aluno PK
- int ano PK
- int semestre_ano PK
- int semestre_curso PK
- string periodo PK


