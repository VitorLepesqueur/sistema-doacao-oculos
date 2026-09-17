CREATE DATABASE IF NOT EXISTS doacao_oculos
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE doacao_oculos;

CREATE TABLE IF NOT EXISTS pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    protocolo VARCHAR(40) NOT NULL UNIQUE,
    nome_solicitante VARCHAR(150) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    telefone VARCHAR(30) NOT NULL,
    rg VARCHAR(30) NOT NULL,
    data_nascimento DATE NOT NULL,
    nome_crianca VARCHAR(150) NOT NULL,
    status ENUM('Pedido feito', 'Pedido em produção', 'Pedido entregue')
        NOT NULL DEFAULT 'Pedido feito',
    data_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mensagens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefone VARCHAR(30),
    tipo VARCHAR(80) NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


INSERT IGNORE INTO pedidos
(protocolo, nome_solicitante, endereco, telefone, rg, data_nascimento,
 nome_crianca, status, data_pedido, atualizado_em)
VALUES
('pedido1', 'João Carlos de Souza Mendes', 'Rua das Flores, 120', '(38) 99915-2406', 'MG-15.244.789', '1993-04-11', 'Lucas Souza Mendes', 'Pedido entregue', '2026-08-05 09:10:00', '2026-08-15 16:30:00'),
('pedido2', 'Sebastião de Oliveira Santos', 'Av. Governador Valadares, 1001', '(38) 99899-1052', 'MG-11.156.657', '1988-09-20', 'Ana Luiza Oliveira Santos', 'Pedido entregue', '2026-08-09 14:20:00', '2026-08-22 10:05:00'),
('pedido3', 'Maria da Conceição Borges', 'Rua Djalma Torres, 789', '(38) 99988-2507', 'MG-11.157.625', '1995-01-17', 'Pedro Jorge Borges', 'Pedido entregue', '2026-08-14 11:45:00', '2026-08-28 15:00:00'),


('pedido4', 'Roberto Aguiar Louzada', 'Rua Dona Dezinha 125', '(38) 99899-1254', 'MG-11.623.987', '1991-07-02', 'Beatriz Aguiar Louzada', 'Pedido em produção', '2026-09-02 08:50:00', '2026-09-10 13:20:00'),
('pedido5', 'Ricardo Alves Santana', 'Rua Nossa Senhora do Carmo, 301', '(38) 99891-1545', 'MG-13.741.152', '1986-12-29', 'Gabriel Alves Santana', 'Pedido em produção', '2026-09-05 10:35:00', '2026-09-12 09:40:00'),


('pedido6', 'Patrícia Gomes Cordeiro', 'Av. José Luiz Adjuto, 1153', '(38) 99912-2530', 'MG-14.156.231', '1990-03-08', 'Sofia Gomes Cordeiro', 'Pedido feito', '2026-09-14 17:05:00', '2026-09-14 17:05:00');
