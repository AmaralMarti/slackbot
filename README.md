
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

# Dependencias

SlackClient https://github.com/slackhq/python-slackclient

Blinker https://github.com/jek/blinker

# Exemplo de uilização
<pre><code>
#!/usr/bin/python
# coding=utf-8

from slackBot import SlackBot as Bot
import time


def tratar_hello(self):
    print 'Hello'


def tratar_presenca(self):
    print 'Presença'


def tratar_url_reconnect(self):
    print 'URL Reconnect'


def tratar_digitando(self, data):
    user_info = bot.get_user_info(data['user'])
    channel_info = bot.get_channel_info(data['channel'])
    print user_info['name'], 'está digitando no canal', channel_info['name']


def tratar_mensagens(self, data):
    message = ''
    if 'text' in data.keys():
        message = data['text']
    user_info = bot.get_user_info(data['user'])
    channel_info = bot.get_channel_info(data['channel'])

    if bot.user['name'] in message:
        resposta = 'Falou comigo ' + str(user_info['name']) + '?'
        bot.slackClient.rtm_send_message(channel=channel_info['id'], message=resposta)

    if message == '$ListarMembros':
        if channel_info['type'] != 'is_im':
            bot.slackClient.rtm_send_message(channel=channel_info['id'], message='Vou providenciar os dados senhor ' + str(user_info['name']) + '...')
            members = bot.channel_members(channel_info['id'])
            if len(members) > 0:
                resposta = ''
                for member in members:
                    member_info = bot.get_user_info(member)
                    resposta += member_info['name'] + '\n'
                bot.slackClient.rtm_send_message(channel=channel_info['id'], message=resposta)
            else:
                bot.slackClient.rtm_send_message(channel=channel_info['id'], message='Não foi possivel processar')
        else:
            bot.slackClient.rtm_send_message(channel=channel_info['id'], message='Estamos em uma conversa direta, só há nós dois aqui')

    if message == '$ListarUsuarios':
        bot.slackClient.rtm_send_message(channel=channel_info['id'], message='Vou providenciar os dados senhor ' + str(user_info['name']) + '...')
        users = bot.user_list()
        resposta = ''
        for user in users:
            resposta += user['name'] + '\n'
        bot.slackClient.rtm_send_message(channel=channel_info['id'], message=resposta)

    print 'Mensagem de', user_info['name'], 'no canal', channel_info['name'] + ':'
    print message


def get_token():
    bot_token = open('token.txt', 'r')
    try:
        return bot_token.read()
    finally:
        bot_token.close()

# O programa é iniciado aqui
if __name__ == "__main__":

    token = get_token().strip()

    # Cria o objeto do BOT
    try:
        bot = Bot(token)
    except Exception as e:
        bot = None
        print e.message
        exit()

    # Log com os dados do Time e do Bot
    print 'Slack Bot conectado com sucesso!'
    print ''
    print 'Team:', bot.team['name']
    print 'User:', bot.user['name']
    print ''
    print ''

    # Atribui os métodos para tratar cada tipo de evento
    bot.OnHelloEvent.connect(tratar_hello)
    bot.OnPresenceChangeEvent.connect(tratar_presenca)
    bot.OnReconnectUrlEvent.connect(tratar_url_reconnect)
    bot.OnUserTypingEvent.connect(tratar_digitando)
    bot.OnMessageEvent.connect(tratar_mensagens)

    bot.eventMonitor.start()

    print 'Para encerrar pressione CTRL+C'
    try:
        while True:
            time.sleep(0.3)
    except:
        print '\nExecução finalizada!'
        bot.destroy()
        exit()
 </code></pred>
