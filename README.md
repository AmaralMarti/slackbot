# slackbot
Esse módulo permite criar um programa para comandar um Bot User no Slack. Para saber o que é um Bot User e como criar o seu, 
acesse https://api.slack.com/bot-users

No arquivo "Demo.py" você pode ver um exemplo bem simples de como usar esse módulo, mas os passos básicos necessários são:

 - Criar o objeto
 - Atribuir os métodos de tratamento dos eventos que você deseja tratar
   (OnHelloEvent, OnPresenceChangeEvent, OnUserTypingEvent, OnMessageEvent, etc)
 

o que se resume basicamente em criar o
objeto, atribuir os métodos que vão tratar os eventos que você deseja monitorar  iniciar o monitor de eventos (o que faz o Bot User ficer com status "online" no Slack)

Há também métodos para:
 - Listar os canais públicos do time
 - Listar os canais fechados que o Bot User participa
 - Listar os chats em que o Bot User está
 - Listar as conversar diretas do Bot User com com outros membros do time
 - 
