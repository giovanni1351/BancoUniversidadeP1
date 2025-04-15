
----------------------------------------------- | Querys Obrigatórias | -----------------------------------------------
/*
1) Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte

;with cte as(
    select
        a.id as aluno
        ,d.id as disciplina
        ,count(distinct c.status) as contagem
    from alunos a
    inner join aluno_historico_escolar b on a.id = b.id_aluno
    inner join historico_escolar c on c.id = b.id_historico_escolar
    inner join disciplinas d on d.id = c.id_disciplina
    where 1 = 1
        and a.nome = 'Alexandre da Paz'
    group by a.id, d.id
    )
        
    select
    distinct
        a.nome as Nome_Aluno
        ,d.nome as Nome_Disciplina
    ,c.status
    from alunos a
    inner join aluno_historico_escolar b on a.id = b.id_aluno
    inner join historico_escolar c on c.id = b.id_historico_escolar
    inner join disciplinas d on d.id = c.id_disciplina
    inner join cte e on a.id = e.aluno
    where 1 = 1
    and e.contagem = 2
    order by 1, 2
*/
/*
2) Mostre todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto;
    SELECT 
        a.titulo,
        a.tema,
        a.nota,
        b.nome as nome_professor,
        c.nome as nome_alunos,
        a.id as id_tcc
    FROM tcc a
    LEFT JOIN professores b on a.id_professor = b.id
    LEFT JOIN alunos c on a.id = c.id_tcc
    WHERE 1 = 1
        and b.nome = 'Eloá Cassiano'
*/
/*
3) Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum 
(e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso
    with cte as (
        select 
        a.*,
        b.nome as nome_curso,
        b.codigo,
        c.nome as nome_disciplina,
        row_number() over (partition by c.id order by b.id) as dp
        from matriz_curricular a
        LEFT JOIN curso b on a.id_curso = b.id
        LEFT JOIN disciplinas c on a.id_disciplina = c.id
    )

    select 
        * 
    from cte 
    where 1 = 1
        and dp > 1
    order by 
        id_disciplina
*/
/*
4) Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno;
    SELECT 
        b.nome as nome_aluno,
        c.nome as nome disciplinas,
        a.id_disciplina as cod_disciplina,
        e.nome as nome_professor
    FROM disciplinasalunos a
    LEFT JOIN alunos b on a.id_aluno = b.id
    LEFT JOIN disciplinas c on a.id_disciplina = c.id
    LEFT JOIN professores_disciplinas d on c.id = d.id_disciplina
    LEFT JOIN professores e on d.id_professor = e.id
*/
