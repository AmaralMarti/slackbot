#!/usr/bin/python
# coding=utf-8

from slackBot import SlackBot as Bot


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
        if channel_info['type'] != 'im':
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

    token = get_token()

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

    while True:
        # Apresenta um menu com as opções disponíveis
        print '1 - Start Slack Monitor'
        print '2 - Stop Slack Monitor'
        print '3 - Exit'
        cmd = raw_input('>')

        if cmd == '1':
            # Inicia o Monitor de Eventos do Slack
            bot.eventMonitor.start()

        if cmd == '2':
            # Para o Monitor de Eventos do Slack
            bot.eventMonitor.stop()

        if cmd == '3':
            print 'Execução finalizada!'
            bot.destroy()
            exit()
