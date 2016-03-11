# coding=utf-8

from slackclient import SlackClient
from slackBotEventMonitor import slackBotEventMonitor
from slackBotInfo import slackBotInfo
from blinker import Signal


class slackBot:
    """Classe que define o BOT para Slack.
    O parametro "token" deve ser preenchido com o token do seu "bot user"
    (para ver como criar um "bot user" acesse https://api.slack.com/bot-users)"""

    def __init__(self, token):

        self.user = dict()
        self.team = dict()

        self.slackClient = SlackClient(token)
        response = self.slackClient.api_call('auth.test')

        if response['ok']:
            # Carrega os dado do Usuário (o próprio BOT)
            self.user['id'] = response['user_id']
            self.user['name'] = response['user']

            # Carrega os dado do Time
            self.team['id'] = response['team_id']
            self.team['name'] = response['team']
        else:
            error = response['error']
            if response['error'] == 'not_authed':
                error = 'No authentication token provided.'
            if response['error'] == 'invalid_auth':
                error = 'Invalid authentication token.'
            if response['error'] == 'account_inactive':
                error = 'Authentication token is for a deleted user or team.'
            if response['error'] == 'request_timeout':
                error = 'Timeout.'

            raise Exception(error)

        # Criacao dos manipuladores de eventos recebidos do Slack
        self.OnHelloEvent = Signal(slackBotEventMonitor.HELLO_EVENT)
        self.OnPresenceChangeEvent = Signal(slackBotEventMonitor.PRESENCE_CHANGE_EVENT)
        self.OnReconnectUrlEvent = Signal(slackBotEventMonitor.RECONNECT_URL_EVENT)
        self.OnUserTypingEvent = Signal(slackBotEventMonitor.USER_TYPING_EVENT)
        self.OnMessageEvent = Signal(slackBotEventMonitor.MESSAGE_EVENT)

        self.eventMonitor = slackBotEventMonitor(self)
        self.__info = slackBotInfo(self)
        self.__info.start()

    def destroy(self):
        self.eventMonitor.destroy()
        self.__info.active = False

    def getUserInfo(self, id):
        return self.__info.getUseInfo(id)

    def getChannelInfo(self, id):
        return self.__info.getChannelInfo(id)

    def channelList(self):
        """Metodo que retorna uma lista com todos os canais publicos do canal.
        Cada item da lista e um dicionario com os detalhes de cada canal publico.
        (para mais informacoes veja acesse https://api.slack.com/types/channel)"""
        return self.slackClient.api_call('channels.list')['channels']

    def groupList(self):
        """Metodo que retorna uma lista com todos os canais privados que o usuario particisa.
        Cada item da lista e um dicionario com os detalhes de cada canal privado.
        (para mais informacoes veja https://api.slack.com/types/group)"""
        return self.slackClient.api_call('groups.list')['groups']

    def mpimList(self):
        """Metodo que retorna uma lista com todos os chats (conversas multiusuario) que o usuario participa.
        Cada item da lista e um dicionario com os detalhes de cada chat.
        (para mais informacoes veja https://api.slack.com/types/mpim)"""
        return self.slackClient.api_call('mpim.list')['groups']

    def imList(self):
        """Metodo que retorna uma lista com todas as "Direct Messages" que o usuario participa.
        Cada item da lista e um dicionario com os detalhes de cada conversa.
        (para mais informacoes veja https://api.slack.com/types/im)"""
        return self.slackClient.api_call('im.list')['ims']

    def userList(self):
        """Metodo que retorna uma lista com todos os usuario que pertencem ao time. Cada item da lista e um
        dicionario com os detalhes de cada usuario
        (para mais informacoes veja https://api.slack.com/types/user)"""
        return self.slackClient.api_call('users.list')['members']

    def channelMembers(self, channelId):
        """Metodo que retorna uma lista com os IDs dos membros do canal indicado
        (para mais informacoes veja https://api.slack.com/methods/channels.info)"""
        result = self.slackClient.api_call('channels.info', channel=channelId)
        if result['ok']:
            return result['channel']['members']

        result = self.slackClient.api_call('groups.info', channel=channelId)
        if result['ok']:
            return result['group']['members']
