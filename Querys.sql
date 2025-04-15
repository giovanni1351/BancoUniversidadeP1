
----------------------------------------------- | Querys Obrigatórias | -----------------------------------------------
/*
1) Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte
    SELECT 
        b.nome as nome_aluno,
        c.nome as nome_disciplina,
        a.semestre_ano,
        e.nota,
        e.status
    FROM disciplinasalunos a
    LEFT JOIN alunos b on a.id_aluno = b.id
    LEFT JOIN disciplinas c on a.id_disciplina = c.id
    LEFT JOIN aluno_historico_escolar d on a.id_aluno = d.id_aluno
    LEFT JOIN historico_escolar e on d.id_historico_escolar = e.id
    WHERE 1 = 1
        and b.nome = 'Rafael Moura'
        and e.status = 'Trancado' -- quando Givas fizer alteracao trocar por 'Reprovado'
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
