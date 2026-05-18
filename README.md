# O-Assombro 👻

Projeto da disciplina SCC0250 – Computação Gráfica, com foco na construção de um cenário 3D interativo e imersivo. A proposta é criar uma experiência visual baseada em tensão e desconforto, explorando elementos visuais para provocar uma sensação constante de inquietação no usuário.

---

## Descrição

O-Assombro é um cenário tridimensional composto por ambientes interno e externo, projetado para ser explorado livremente pelo usuário por meio da manipulação da câmera. A cena busca transmitir uma atmosfera horripilante através da composição dos objetos, texturas e organização espacial.

> Este documento será atualizado conforme novas funcionalidades forem implementadas (controles, interações, efeitos).

---

## Objetivo

- Desenvolver um ambiente 3D navegável
- Aplicar conceitos de transformação geométrica (Model, View e Projection)
- Utilizar modelos com textura em uma cena coerente
- Criar uma experiência imersiva com foco em tensão

---

## Estrutura do Projeto

| Componente        | Descrição                                      |
|------------------|-----------------------------------------------|
| Ambiente Interno | Espaço fechado ()      |
| Ambiente Externo | Espaço aberto ()        |
| Modelos 3D       | Objetos importados em formato `.obj`          |
| Texturas         | Imagens aplicadas aos modelos                 |
| Câmera           | Sistema de navegação no cenário               |

---

## Funcionalidades (em desenvolvimento)

| Funcionalidade              | Status       | Observações                     |
|----------------------------|-------------|--------------------------------|
| Movimentação da câmera     | Implementado   |  Desabilitar simulação de caminhada com 'H'|
| Controles via teclado      | Implementado    |                                |
| Alternância de malha (wireframe) | Implementado | Tecla 'P'                      |
| Transformações (escala, rotação, translação) | Implementado | Controle individual por modelo |
| Iluminação interativa | Implementado | Lanternas, faróis e velas controlados pelo teclado |

---

## Controles

| Ação                  | Tecla        |
|----------------------|-------------|
| Caminhar pela cena          | A W S D |
| Movimento vertical câmera | Setas cima / baixo |
| Translação carro | Setas esquerda / direita |
| Rotação da abóbora | I / K |
| Rotação cadeira | R / F |
| Translação cadeira | T / G |
| Translação mesa | Y / B |
| Escala fantasma | U / J |
| Escala e translação menina | Jumpscare! |
| Ligar/desligar lanterna da mão | 1 |
| Ligar/desligar faróis do carro | 2 |
| Ligar/desligar luz das velas | 3 |
| Diminuir intensidade da lanterna da mão | 4 |
| Aumentar intensidade da lanterna da mão | 5 |
| Alternar luz das velas entre amarela e branca | 6 |

---

## Requisitos do Projeto

- Cenário com ambiente interno e externo
- Mínimo de 6 modelos 3D distintos com textura
- Distribuição dos modelos entre os ambientes
- Aplicação de transformações geométricas
- Implementação de navegação por câmera
- Uso de arquivos `.obj`
- Renderização com pipeline moderno do OpenGL
- Sem uso de iluminação

---

## Observações

- Os modelos devem respeitar proporções realistas
- Cada objeto deve ser importado de um arquivo separado
- O cenário deve possuir coerência visual e temática
- A câmera deve permanecer dentro dos limites do cenário

---

## Autoras

- Catarina Moreira Lima - Nº USP: 8957221
- Eduarda Almeida Garrett de Carvalho - Nº USP: 14566794
