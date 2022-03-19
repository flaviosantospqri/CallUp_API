<h1 align="center">
  CallUp - API
</h1>

<p align = "justify">
  A CallUp - API foi desenvolvida com o propósito de facilitar e melhorar a experiência das empresas e de seus funcionários dando a eles comodidade e agilidade na hora de solucionar suas demandas e necessidades de suporte técnico diários. Toda empresa em algum momento vai precisar de um técnico especializado para cuidar de algum problema ou simplesmente um serviço, com este intuito estamos desenvolvendo a CallUp, uma plataforma onde uma empresa pode abrir um chamado e aguardar até que um dos prestadores de serviço faça uma proposta para aquela demanda. Imagine em um único lugar você já ter orçamentos, cotações e o melhor, profissionais treinados e especializados. Em contra partida, o prestador vai ter em suas mãos as principais demandas que estão de acordo com suas especialidades.
</p>

<p align="center">
  <a href="#endpoints">Endpoints</a>
</p>

## **Endpoints**

A API tem um total de 11 endpoints, sendo em volta principalmente do usuário - que poderá cadastrar seu perfil, listar restaurantes, favoritos. <br/>

O url base da API é https://callup-capq3.herokuapp.com/



<h2 align ='center'> Categorias </h2>


## Rota que não precisa de autenticação


`GET /categories - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /categories - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "id": "447a3c4f-5542-4ec9-90c5-e8717d81765a",
    "name": "System Analysis"
  },
  {
    "id": "48861533-8db0-4e25-b37a-5738afb17ad4",
    "name": "Networks"
  },
]
```


<h2 align ='center'> Subcategorias </h2>


## Rota que não precisa de autenticação


`GET /subcategories - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /subcategories - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "id": "d6f1ba0e-4164-4d6c-b0fd-be100e87224c",
    "name": "Performance Analysis"
  },
  {
    "id": "1c56af50-f9d8-485d-86f0-1a268283576c",
    "name": "Feature Analysis"
  },
]
```


<h2 align ='center'> Setores </h2>


## Rota que não precisa de autenticação


`GET /sectors - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /sectors - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "id": "3820a99f-d409-4c60-a25d-e0fe464a265a",
    "name": "Governing"
  },
  {
    "id": "71681d4d-7d28-4339-9f10-3fb950caca78",
    "name": "Financial"
  },
]
```


<h2 align ='center'> Empresas </h2>


## Rotas que não precisam de autenticação


<h3 align = "center"> Register </h3>

`POST /companies - FORMATO DA REQUISIÇÃO`

```json
{
	"name": "Callup SA",
	"cnpj": "00.000.000/0001-00",
	"address": "Rua da kenzie",
	"email": "callup@gmail.com",
	"password": "Teste123!"
}
```

    Caso dê tudo certo, a resposta será assim:

`POST /companies - FORMATO DA RESPOSTA - STATUS 201`

```json
{
  "address": "Rua da kenzie",
  "cnpj": "00.000.000/0001-00",
  "email": "callup@gmail.com",
  "id": "bf1791cc-3545-47f3-b38a-5bf28a249c5a",
  "name": "Callup Sa",
  "type": "company"
}
```


<h3 align = "center"> Login </h3>

`POST /companies/login - FORMATO DA REQUISIÇÃO`

```json
{
	"email": "callup@gmail.com",
	"password": "Teste123!"
}
```


    Caso dê tudo certo, a resposta será assim:

`POST /companies/login - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0Njk1MjMyMiwianRpIjoiNzc1MmQyMmUtNDIxYy00ZmZkLTg2NGQtYjBhMWM0ZjBmMTI5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6ImJmMTc5MWNjLTM1NDUtNDdmMy1iMzhhLTViZjI4YTI0OWM1YSIsIm5hbWUiOiJDYWxsdXAgU2EiLCJjbnBqIjoiMDAuMDAwLjAwMC8wMDAxLTAwIiwiZW1haWwiOiJjYWxsdXBAZ21haWwuY29tIiwiYWRkcmVzcyI6IlJ1YSBkYSBrZW56aWUiLCJ0eXBlIjoiY29tcGFueSJ9LCJuYmYiOjE2NDY5NTIzMjIsImV4cCI6MTY0Njk1MzIyMn0.y2MxvQJEyfDaLSi3SQ3UbLA3K2n44t8Mq-ihirs4i_U"
}
```


## Rotas que necessitam de autenticação


Rotas que necessitam de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma:

> Authorization: Bearer {token}


<h3 align = "center"> Ver dados da empresa </h3>


`GET /companies - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /companies - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "address": "Rua da kenzie",
  "cnpj": "00.000.000/0001-00",
  "email": "callup@gmail.com",
  "employees": [],
  "id": "bf1791cc-3545-47f3-b38a-5bf28a249c5a",
  "name": "Callup Sa"
}
```

<h3 align = "center"> Ver chamados da empresa em PDF </h3>


`GET /companies/pdf - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /companies/pdf - FORMATO DA RESPOSTA - STATUS 200`

```json
{"stts": "ok"}
```

<h3 align = "center"> Alterar dados cadastrais da empresa </h3>


`PATCH /companies - FORMATO DA REQUISIÇÃO`

```json
{
	"address": "Rua do Mcdonalds"
}
```

    Caso dê tudo certo, a resposta será assim:

`PATCH /companies - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "address": "Rua do Mcdonalds",
  "cnpj": "00.000.000/0001-00",
  "email": "callup@gmail.com",
  "id": "63d356c7-97e3-4e93-b577-a5370c27c856",
  "name": "Callup Sa",
  "type": "company"
}
```

<h3 align = "center"> Deletar empresa </h3>


`DELETE /companies - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`DELETE /companies - FORMATO DA RESPOSTA - STATUS 200`



## Rotas que não precisam de autenticação


<h3 align = "center"> Register </h3>


`POST /providers - FORMATO DA REQUISIÇÃO`

```json
{
	"name": "Teste1",
	"cnpj": "00000000000000",
	"email": "teste1@mail.com",
	"about": "Alguma coisa qualquer",
	"password": "Juni@r10"
}
```

    Caso dê tudo certo, a resposta será assim:

`POST /companies - FORMATO DA RESPOSTA - STATUS 201`

```json
{
  "about": "Alguma coisa qualquer",
  "cnpj": "00000000000000",
  "email": "teste1@mail.com",
  "id": "bf2b3818-41be-4991-b478-d92a546909b8",
  "name": "Teste1",
  "type": "provider"
}
```

<h3 align = "center"> Login </h3>


`POST /companies/login - FORMATO DA REQUISIÇÃO`

```json
{
	"email": "teste1@mail.com",
	"password": "Juni@r10"
}
```


    Caso dê tudo certo, a resposta será assim:

`POST /companies - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0Njk2NjM2OSwianRpIjoiYWRhMDg5YTktYThjNC00YWM0LTg4M2UtN2VjNWY1YTBhZTU2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6ImJmMmIzODE4LTQxYmUtNDk5MS1iNDc4LWQ5MmE1NDY5MDliOCIsIm5hbWUiOiJUZXN0ZTEiLCJjbnBqIjoiMDAwMDAwMDAwMDAwMDAiLCJhYm91dCI6IkFsZ3VtYSBjb2lzYSBxdWFscXVlciIsImVtYWlsIjoidGVzdGUxQG1haWwuY29tIiwidHlwZSI6InByb3ZpZGVyIn0sIm5iZiI6MTY0Njk2NjM2OSwiZXhwIjoxNjQ2OTY5OTY5fQ.61w0wfzb1c45h28PV9-p9ZS6qa-9aNTjAkYsxAATz2E"
}
```

## Rotas que necessitam de autenticação


Rotas que necessitam de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma:

> Authorization: Bearer {token}


<h3 align = "center"> Ver todas as prestadoras de serviços </h3>


`GET /providers - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /providers - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "about": "Alguma coisa qualquer",
    "cnpj": "00000000000000",
    "email": "teste1@mail.com",
    "id": "bf2b3818-41be-4991-b478-d92a546909b8",
    "name": "Teste1",
    "type": "provider"
  },
  {
    "about": "Alguma coisa qualquer",
    "cnpj": "00000000000001",
    "email": "teste2@mail.com",
    "id": "63e9bec9-8b46-4c3b-838d-182cb6cc53f1",
    "name": "Teste2",
    "type": "provider"
  },
]
```

<h3 align = "center"> Ver prestadora de serviço por CNPJ </h3>


`GET /providers/00000000000000 - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /providers/00000000000000 - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "about": "Alguma coisa qualquer",
  "cnpj": "00000000000000",
  "email": "teste1@mail.com",
  "id": "02915a11-a336-434e-a2cd-00324d105c75",
  "name": "Teste1",
  "type": "provider"
}
```

<h3 align = "center"> Alterar dados cadastrais da pestadora de serviços </h3>


`PATCH /providers - FORMATO DA REQUISIÇÃO`

```json
{
	"about": "Mudando qualquer coisa"
}
```
    Caso dê tudo certo, a resposta será assim:

`PATCH /providers - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "about": "Mudando qualquer coisa",
  "cnpj": "00000000000000",
  "email": "teste1@mail.com",
  "id": "bf2b3818-41be-4991-b478-d92a546909b8",
  "name": "Teste1",
  "type": "provider"
}
```

<h3 align = "center"> Deletar prestadora de serviços </h3>


`DELETE /providers - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`DELETE /providers - FORMATO DA RESPOSTA - STATUS 200`



<h2 align ='center'> Empregados </h2>


## Rotas que necessitam de autenticação


Rotas que necessitam de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma:

> Authorization: Bearer {token}

<h3 align = "center"> Register </h3>


`POST /employees - FORMATO DA REQUISIÇÃO`

```json
{
	"sector": "Human_resources",
	"email": "bia@teste.com",
	"password": "Potato1!",
	"name": "Beatris",
	"phone": "(41)99999-9999"
}
```

    Caso dê tudo certo, a resposta será assim:

`POST /employees - FORMATO DA RESPOSTA - STATUS 201`

```json
{
  "company_id": "6227cd3e-c7ed-4b9f-9bfb-26bfa87d92a4",
  "email": "bia@teste.com",
  "id": "4535b3a2-cfe0-463e-af7b-6b43b062ffd0",
  "name": "Beatris",
  "phone": "(41)99999-9999",
  "sector": {
    "name": "Human_resources"
  },
  "type": "employee"
}
```

<h3 align = "center"> Login </h3>


`POST /employees/login - FORMATO DA REQUISIÇÃO`

```json
{
	"email": "testefunc@teste.com",
	"password": "Potato1!"
}
```


    Caso dê tudo certo, a resposta será assim:

`POST /employees - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0NzAwNjgyNSwianRpIjoiMzQyNDI2ZTktYjBjYi00OWZiLTg3OTEtYTY0YjkxN2E0MDZiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6IjFlMTYyYjYyLTJiNGQtNDhiOC1iMTY4LWUwY2ZiODNmNmJlMCIsIm5hbWUiOiJQb3RhdG8iLCJjb21wYW55X2lkIjpudWxsLCJwaG9uZSI6Iig0MSk5OTk5OS05OTk5IiwiZW1haWwiOiJ0ZXN0ZWZ1bmNAdGVzdGUuY29tIiwidHlwZSI6ImVtcGxveWVlIiwic2VjdG9yIjp7Im5hbWUiOiJHb3Zlcm5pbmcifX0sIm5iZiI6MTY0NzAwNjgyNSwiZXhwIjoxNjQ3MDEwNDI1fQ.ijNRbokRf3oPjFurPeEBlNnrYX5fAxKd8YLSXez6sZA"
}
```

<h3 align = "center"> Pegar todos os funcinário da empresa</h3>

`GET /employees - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /employees - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "company_id": "6227cd3e-c7ed-4b9f-9bfb-26bfa87d92a4",
    "email": "testefuncinnary@teste.com",
    "id": "2a209ee5-bdfd-4602-b496-c4cf764811ed",
    "name": "Funcionario Brabo",
    "phone": "(41)99999-9999",
    "sector": {
      "name": "Governing"
    },
    "type": "employee"
  },
  {
    "company_id": "6227cd3e-c7ed-4b9f-9bfb-26bfa87d92a4",
    "email": "potato@teste.com",
    "id": "003061fa-b9d4-4eb8-b135-3c52d6b46e23",
    "name": "Potato Master",
    "phone": "(41)99999-9999",
    "sector": {
      "name": "Commercial"
    },
    "type": "employee"
  }
]
```

<h3 align = "center"> Pegar dados do funcionário por email</h3>

`GET /providers/bia@teste.com - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /providers/bia@teste.com - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "company_id": "6227cd3e-c7ed-4b9f-9bfb-26bfa87d92a4",
  "email": "bia@teste.com",
  "id": "4535b3a2-cfe0-463e-af7b-6b43b062ffd0",
  "name": "Biazinha",
  "phone": "(41)99999-9999",
  "sector": {
    "name": "Human_resources"
  },
  "type": "employee"
}
```

<h3 align = "center"> Atualizar dados do funcionário </h3>

`PATCH /providers - FORMATO DA REQUISIÇÃO`

```json
{
	"name": "Biazinha"
}
```
    Caso dê tudo certo, a resposta será assim:

`PATCH /providers - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "company_id": "6227cd3e-c7ed-4b9f-9bfb-26bfa87d92a4",
  "email": "bia@teste.com",
  "id": "4535b3a2-cfe0-463e-af7b-6b43b062ffd0",
  "name": "Biazinha",
  "phone": "(41)99999-9999",
  "sector": {
    "name": "Human_resources"
  },
  "type": "employee"
}
```

<h3 align = "center"> Deletar funcinário </h3>


`DELETE /providers/bia@teste.com - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`DELETE /providers/bia@teste.com - FORMATO DA RESPOSTA - STATUS 200`



<h2 align ='center'> Chamados </h2>


## Rotas que necessitam de autenticação


Rotas que necessitam de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma:

> Authorization: Bearer {token}

<h3 align = "center"> Criar chamado </h3>


`POST /calls - FORMATO DA REQUISIÇÃO`

```json
{
	"category": "Support",
	"subcategory": "Repair",
	"description": "Sitema não esta rodando"
}
```

    Caso dê tudo certo, a resposta será assim:

`POST /calls - FORMATO DA RESPOSTA - STATUS 201`

```json
{
  "description": "Sitema não esta rodando",
  "id": "bec0eafe-6d41-44e1-8fd2-7dc5126adc7c",
  "open": true,
  "selected_proposal": null
}
```

<h3 align = "center"> Pegar todos os chamados da empresa</h3>

`GET /calls - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /calls - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "description": "Modem não funciona e agr ta apitando",
    "id": "0fb66193-cb01-4645-b7d5-a529b3147622",
    "open": true,
    "selected_proposal": null
  },
  {
    "description": "Pc parou de funcionar",
    "id": "32cbc8a0-9777-40b5-a96e-7d586d632a9e",
    "open": true,
    "selected_proposal": null
  }
]
```

<h3 align = "center"> Pegar chamado por email do funcionario que criou</h3>

`GET /calls/bia@teste.com - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /calls/bia@teste.com - FORMATO DA RESPOSTA - STATUS 200`

```json
  {
    "description": "Pc parou de funcionar",
    "id": "5a315450-0918-4678-a791-0ffe09f52a3d",
    "open": true,
    "selected_proposal": null
  },
  {
    "description": "Monitor queimou",
    "id": "523ae0c8-ae15-47b9-9325-210f12d9984f",
    "open": true,
    "selected_proposal": null
  }
```

<h3 align = "center"> Atualizar informações do chamado por ID </h3>

`PATCH /calls/0fb66193-cb01-4645-b7d5-a529b3147622 - FORMATO DA REQUISIÇÃO`

```json
{
	"description": "Modem não funciona e agr ta apitando"
}
```
    Caso dê tudo certo, a resposta será assim:

`PATCH /calls/0fb66193-cb01-4645-b7d5-a529b3147622s - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "description": "Modem não funciona e agr ta apitando",
  "id": "1c964684-e1cf-439f-94d3-fe820ac8caa3",
  "open": true,
  "selected_proposal": null
}
```

<h3 align = "center"> Deletar funcinário </h3>


`DELETE /calls/0fb66193-cb01-4645-b7d5-a529b3147622 - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`DELETE /calls/0fb66193-cb01-4645-b7d5-a529b3147622 - FORMATO DA RESPOSTA - STATUS 200`


<h2 align ='center'> Propostas </h2>


## Rotas que necessitam de autenticação


Rotas que necessitam de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma:

> Authorization: Bearer {token}

<h3 align = "center"> Criar chamado </h3>


`POST /proposals - FORMATO DA REQUISIÇÃO`

```json
{
	"price": 65.6,
	"description": "Orçamento",
	"call_id": "bec0eafe-6d41-44e1-8fd2-7dc5126adc7c"
}
```

    Caso dê tudo certo, a resposta será assim:

`POST /proposals - FORMATO DA RESPOSTA - STATUS 201`

```json
{
  "description": "Orçamento",
  "id": "2596c234-eb75-453c-abba-55579afb2709",
  "price": 65.6
}
```

<h3 align = "center"> Pegar todos as propostas para empresa</h3>

`GET /proposals - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /proposals - FORMATO DA RESPOSTA - STATUS 200`

```json
[
  {
    "description": "alguma coisa",
    "id": "ce6a22a7-cd13-480b-bed2-6763c8807703",
    "price": 659.9
  },
  {
    "description": "alguma coisa",
    "id": "59b68cf3-65d2-454f-9159-2928110ad532",
    "price": 659.9
  },
  {
    "description": "alguma coisa",
    "id": "a0d7cfcb-e4e4-45cb-8755-8c977156a0fa",
    "price": 659.9
  }
]
```

<h3 align = "center"> Pegar todos as propostas aceitas pelas empresa feitas pelas prestadoras de serviço</h3>

`GET /proposals - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`GET /proposals - FORMATO DA RESPOSTA - STATUS 200`

```json
[]
```

<h3 align = "center"> Atualizar informações proposta por ID do chamado </h3>

`PATCH /e0f3ed9a-8caf-4991-b8c5-4cf74b442f52 - FORMATO DA REQUISIÇÃO`

```json
{
	"description": "Modem não funciona e agr ta apitando"
}
```
    Caso dê tudo certo, a resposta será assim:

`PATCH /e0f3ed9a-8caf-4991-b8c5-4cf74b442f52s - FORMATO DA RESPOSTA - STATUS 200`

```json
{
  "description": "Orcamento recalculado",
  "id": "9c986988-fc91-4055-9c9b-fba59dce92da",
  "price": 659.9
}
```

<h3 align = "center"> Deletar proposta </h3>


`DELETE /e0f3ed9a-8caf-4991-b8c5-4cf74b442f52 - FORMATO DA REQUISIÇÃO`

    Caso dê tudo certo, a resposta será assim:

`DELETE /e0f3ed9a-8caf-4991-b8c5-4cf74b442f52 - FORMATO DA RESPOSTA - STATUS 200`
