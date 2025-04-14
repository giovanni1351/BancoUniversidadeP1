alter table public.tcc 
	add constraint fk_professores_tcc foreign key (id_professor) references professores(id)


;alter table public.professores_disciplinas 
	add constraint fk_professores_disc foreign key (id_professor) references professores(id)


;alter table public.alunos 
	add constraint fk_alunos_tcc foreign key (id_tcc) references tcc(id)


;alter table public.alunos 
	add constraint fk_alunos_curso foreign key (id_curso) references curso(id)


;alter table public.professores_disciplinas 
	add constraint fk_profeDis_dis foreign key (id_disciplina) references disciplinas(id)


;alter table public.disciplinasalunos 
	add constraint fk_disAlunos_Alunos foreign key (id_aluno) references alunos(id)


;alter table public.disciplinasalunos 
	add constraint fk_disAlunos_dis foreign key (id_disciplina) references disciplinas(id)


;alter table public.aluno_historico_escolar 
	add constraint fk_alunoHist_aluno foreign key (id_aluno) references alunos(id)


;alter table public.aluno_historico_escolar 
	add constraint fk_alunoHist_hist foreign key (id_historico_escolar) references historico_escolar(id)


;alter table public.professor_departamento 
	add constraint fk_profDepart_prof foreign key (id_professor) references professores(id)


;alter table public.professor_departamento 
	add constraint fk_profDepart_depart foreign key (id_departamento) references departamento(id)


;alter table public.matriz_curricular 
	add constraint fk_matCu_cu foreign key (id_curso) references curso(id)


;alter table public.matriz_curricular 
	add constraint fk_matCu_dis foreign key (id_disciplina) references disciplinas(id)


;alter table public.historico_escolar 
	add constraint fk_histEsc_disc foreign key (id_disciplina) references disciplinas(id)


;alter table public.disciplinas 
	add constraint fk_disc_depart foreign key (id_departamento) references departamento(id)
