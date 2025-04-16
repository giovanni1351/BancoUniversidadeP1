
------------------------------------------------------------------------ | Querys Solicitadas | ------------------------------------------------------------------------
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
        c.nome as nome_alunos
    FROM tcc a
    INNER JOIN professores b on a.id_professor = b.id
    INNER JOIN alunos c on a.id = c.id_tcc
    WHERE 1 = 1
    --and b.nome = 'nome do professor que voce deseja'
        
*/
/*
3) Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum 
(e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso
    ;with cte as (
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
    nome_curso,
    nome_disciplina 
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
        c.nome as nome_disciplina,
        c.cod_disciplina,
        e.nome as nome_professor
    FROM disciplinasalunos a
    LEFT JOIN alunos b on a.id_aluno = b.id
    LEFT JOIN disciplinas c on a.id_disciplina = c.id
    LEFT JOIN professores_disciplinas d on c.id = d.id_disciplina
    LEFT JOIN professores e on d.id_professor = e.id
    --WHERE b.nome = 'nome do aluno que voce deseja'
*/


/*
5) Liste todos os chefes de departamento e coordenadores de curso em apenas uma query de forma que a primeira coluna seja o nome do professor, 
    a segunda o nome do departamento coordena e a terceira o nome do curso que coordena. 
    Substitua os campos em branco do resultado da query pelo texto "nenhum"

with cte as(
select 
a.nome as nome_professor,
case
  WHEN is_chefe = 'false' then 'nenhum'
  else c.nome
end as departamento,
coalesce(d.nome, 'nenhum') Coordenacao
from professores a
left join professor_departamento b on a.id = b.id_professor
left join departamento c on b.id_departamento = c.id
left join curso d on d.id_professor_cordenador = a.id

)

select * from cte
where 1=1
    and coordenacao <> departamento

*/

------------------------------------------------------------------------ | Querys Selecionadas | ------------------------------------------------------------------------

/*
50) Liste os nomes dos estudantes que não cursaram nenhum curso no departamento de "Engenharia".

;WITH ALUNOS_ENG AS (
	SELECT
		DISTINCT
			A.id AS ID_ALUNO
	FROM alunos A
		INNER JOIN disciplinasalunos B ON A.id = B.id_aluno
		INNER JOIN disciplinas C ON C.id = B.id_disciplina
		INNER JOIN departamento D ON D.id = C.id_departamento
	WHERE 1 = 1
		AND D.NOME = 'Engenharia'
)
SELECT
	DISTINCT
		A.nome
FROM alunos A
LEFT JOIN ALUNOS_ENG B ON A.id = B.id_aluno
WHERE 1 = 1
	AND B.ID_ALUNO IS NULL
*/

/*
47) Recupere os títulos dos cursos e os nomes dos professores que os ministraram, onde o curso tenha pelo menos 5 alunos matriculados.

;WITH CURSOS_SELECIONADOS AS (
	SELECT
		B.id
		,B.nome
		,COUNT(*) AS NUMERO_ALUNOS
	FROM alunos A
	INNER JOIN curso B ON A.id_curso = B.id
	GROUP BY
		B.id, B.nome
	HAVING 
		COUNT(*) > 5
)

SELECT
	DISTINCT
		A.nome AS CURSO
		,E.nome AS PROFESSOR
FROM CURSOS_SELECIONADOS A
INNER JOIN matriz_curricular B ON B.id_curso = A.id
INNER JOIN disciplinas C ON B.id_disciplina = C.id
INNER JOIN professores_disciplinas D ON D.id_disciplina = C.id
INNER JOIN professores E ON D.id_professor = E.id
ORDER BY 
	1

*/

/*
--46. Encontre os estudantes que cursaram "Engenharia de Software" e "Redes de Computadores" no mesmo semestre.

;WITH ALUNOS_SELECIONADOS AS(
	SELECT
		B.id AS id_disciplina
		,A.id_aluno AS id_aluno
		,A.semestre_ano
		,B.nome
		,ROW_NUMBER() OVER(PARTITION BY id_aluno, semestre_ano ORDER BY id_aluno) DP
	FROM disciplinasalunos A
	INNER JOIN disciplinas B ON A.id_disciplina = B.ID
	WHERE 1 = 1
		AND B.nome IN ('Engenharia de Software', 'Redes de Computadores')
)
SELECT
	*
FROM alunos A
INNER JOIN ALUNOS_SELECIONADOS B ON A.ID = B.ID_ALUNO
WHERE 1 = 1
	AND DP = 2
*/

/*
--08. Liste os IDs dos professores que ensinam mais de um curso.
;WITH PROFESSORES_SELECIONADOS AS (
	SELECT
		id_professor
		,COUNT(DISTINCT ID_CURSO)
	FROM professores_disciplinas A
	INNER JOIN matriz_curricular B ON A.id_disciplina = B.id_disciplina
	GROUP BY
		id_professor
	HAVING 
		COUNT(DISTINCT ID_CURSO) > 2
)
SELECT
	id_professor
FROM PROFESSORES_SELECIONADOS
*/

/*
--15. Encontre os estudantes que cursaram "Engenharia de Software" mas não "Engenharia de Computação".

;WITH ALUNOS_ENG_COMP AS (
	SELECT
		id_aluno
	FROM disciplinasalunos A
	INNER JOIN disciplinas B ON A.id_disciplina = B.id
	WHERE 1 = 1
		AND B.NOME = 'Engenharia de Computação'
)
, ALUNOS_ENG_SOFT AS (
	SELECT
		id_aluno
	FROM disciplinasalunos A
	INNER JOIN disciplinas B ON A.id_disciplina = B.id
	WHERE 1 = 1
		AND B.NOME = 'Engenharia de Software'
)
, ALUNOS_SELECIONADOS AS (
	SELECT
		A.*
	FROM ALUNOS_ENG_SOFT A
	LEFT JOIN ALUNOS_ENG_COMP B ON A.ID_ALUNO = B.id_aluno
	WHERE 1 = 1
		AND B.ID_ALUNO IS NULL
)

SELECT
	B.NOME
FROM ALUNOS_SELECIONADOS A
INNER JOIN ALUNOS B ON A.ID_ALUNO = B.ID
*/

/*
--16. Liste todos os cursos que foram cursados por estudantes do departamento de "Ciência da Computação" ou do departamento de "Matemática".

SELECT
	DISTINCT
		E.nome
FROM alunos A 
INNER JOIN disciplinasalunos B ON A.id = B.id_aluno
INNER JOIN disciplinas C ON B.id_disciplina = C.id
INNER JOIN departamento D ON C.id_departamento = D.id
INNER JOIN curso E ON A.id_curso = E.id
WHERE 1 = 1
	AND D.nome IN ('Engenharia de Computação', 'Matemática')
*/

/*
--31. Encontre os nomes dos estudantes que cursaram um curso em todos os departamentos.

SELECT
	 A.id
	,COUNT(D.ID)
FROM alunos A 
INNER JOIN disciplinasalunos B ON A.id = B.id_aluno
INNER JOIN disciplinas C ON B.id_disciplina = C.id
INNER JOIN departamento D ON C.id_departamento = D.id
INNER JOIN curso E ON A.id_curso = E.id
WHERE 1 = 1
GROUP BY
	A.ID
HAVING COUNT(D.ID) = (SELECT COUNT(ID) FROM departamento)
*/

/*
--35. Recupere os nomes dos estudantes que cursaram disciplinas em mais de 3 departamentos.

SELECT
	 A.nome
	,COUNT(C.id_departamento)
FROM alunos A 
INNER JOIN disciplinasalunos B ON A.id = B.id_aluno
INNER JOIN disciplinas C ON B.id_disciplina = C.id
WHERE 1 = 1
GROUP BY
	A.ID
HAVING COUNT(C.id_departamento) > 3
*/

/*
--39. Encontre os nomes dos professores que ministraram cursos nos quais todos os alunos receberam nota '10'.

;WITH CURSOS_SELECIONADOS AS (
	SELECT
		 A.id_curso
		,COUNT(*)
		,SUM(NOTA)
	FROM ALUNOS A
	INNER JOIN curso B ON A.id_curso = B.ID
	INNER JOIN aluno_historico_escolar C ON A.ID = C.id_aluno
	INNER JOIN historico_escolar D ON C.id_historico_escolar = D.ID
	WHERE 1 = 1
	GROUP BY A.id_curso
	HAVING (COUNT(*)*10) = SUM(nota)
	ORDER BY A.id_curso
)
SELECT 
	DISTINCT
		E.nome
FROM CURSOS_SELECIONADOS A
INNER JOIN ALUNOS B ON A.ID_CURSO = B.id_curso
INNER JOIN disciplinasalunos C ON B.id = C.id_aluno
INNER JOIN professores_disciplinas D ON C.id_disciplina = D.id_disciplina
INNER JOIN professores E ON D.id_professor = E.id
*/

/*
--21. Liste os cursos que são ministrados pelo professor 'I001', juntamente com os títulos dos cursos.

SELECT 
	DISTINCT
		A.nome
FROM CURSO A
INNER JOIN ALUNOS B ON A.ID = B.id_curso
INNER JOIN disciplinasalunos C ON B.id = C.id_aluno
INNER JOIN professores_disciplinas D ON C.id_disciplina = D.id_disciplina
INNER JOIN professores E ON D.id_professor = E.id
WHERE 1 = 1
	AND E.id = 2
*/
