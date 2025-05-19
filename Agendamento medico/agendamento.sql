/*CREATE DATABASE projeto_final;

USE projeto_final; 



CREATE TABLE tbl_usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100),
    cpf_usuario VARCHAR(11) UNIQUE,
    email_usuario VARCHAR(100) UNIQUE,
    senha_usuario VARCHAR(100),
    data_nascimento DATE
);

CREATE TABLE tbl_agendamento1 (
    id_agen INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    data_hora DATE,
    horas_agen TIME,
    descricao_agen TEXT,
    FOREIGN KEY (id_usuario) REFERENCES tbl_usuario(id_usuario)
);
CREATE TABLE tbl_medico(
    id_medico INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome_medico VARCHAR(250),
    cargo_medico VARCHAR(250),
    crm_medico VARCHAR(20) 
);*/

SELECT * FROM tbl_agendamento1
;