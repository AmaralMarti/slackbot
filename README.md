# slackbot
Esse módulo permite criar um programa para comandar um Bot User no Slack. Para saber o que é um Bot User e como criar o seu, 
acesse https://api.slack.com/bot-users

No arquivo "Demo.py" você pode ver um exemplo bem simples de como usar esse módulo, mas os passos básicos necessários são:

 - Criar o objeto
 - Atribuir os métodos de tratamento dos eventos que você deseja tratar (OnHelloEvent, OnPresenceChangeEvent,     OnUserTypingEvent, OnMessageEvent, etc)
 - Iniciar o Monitor de Eventos (isso fará o Bot User ficar com status "online" no Slack)
 - Pronto!

 
 O módulo possui também métodos para:
 - Listar os canais públicos do time [channel_list()]
 - Listar os canais fechados que o Bot User participa [group_list()]
 - Listar os chats em que o Bot User está [mpim_list()]
 - Listar as conversar diretas do Bot User com com outros membros do time [im_list()]
 - Listar todos os membros do time [user_list]
 - Listar todos os membros de uma conversa com multiplos usuários (canal público, canals fechado ou chat) [channel_members()]
 - Obter detalhes sobre um usuário [get_user_info()]
 - obter detalhes sobre um canal [get_channel_info()]
  
 Esse módulo já é funcional, mas sem dúvida nenhuma falta muito para estar completo e por isso preciso da sua ajuda para corrigir erros que forem descobertos e aumentar as funcionalidades disponíveis.

Se você gostou desse módulo e quer ajudar no desenvolvimento, você pode dar uma olhada no manual da API do Slack (principalmente https://api.slack.com/methods e https://api.slack.com/rtm), dar uma olhada nas Issues e começar a codificar.
