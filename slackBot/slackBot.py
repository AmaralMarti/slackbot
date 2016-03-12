# coding=utf-8

from slackclient import SlackClient
from slackBotEventMonitor import SlackBotEventMonitor
from slackBotInfo import SlackBotInfo
from blinker import Signal


class SlackBot:
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
        self.OnHelloEvent = Signal(SlackBotEventMonitor.HELLO_EVENT)
        self.OnPresenceChangeEvent = Signal(SlackBotEventMonitor.PRESENCE_CHANGE_EVENT)
        self.OnReconnectUrlEvent = Signal(SlackBotEventMonitor.RECONNECT_URL_EVENT)
        self.OnUserTypingEvent = Signal(SlackBotEventMonitor.USER_TYPING_EVENT)
        self.OnMessageEvent = Signal(SlackBotEventMonitor.MESSAGE_EVENT)

        self.eventMonitor = SlackBotEventMonitor(self)
        self.__info = SlackBotInfo(self)
        self.__info.start()

    def destroy(self):
        self.eventMonitor.destroy()
        self.__info.active = False

    def get_user_info(self, user_id):
        return self.__info.get_user_info(user_id)

    def get_channel_info(self, channel_id):
        return self.__info.get_channel_info(channel_id)

    def channel_list(self):
        """
        Retorna uma lista com todos os canais publicos do time.
        Cada item da lista e um dicionario com os detalhes de cada canal publico.
        (para detalhes sobre o dicionario de retorno veja https://api.slack.com/types/channel)
        """
        return self.slackClient.api_call('channels.list')['channels']

    def group_list(self):
        """
        Retorna uma lista com todos os canais privados que o usuario participa.
        Cada item da lista e um dicionario com os detalhes de cada canal privado.
        (para detalhes sobre o dicionario de retorno veja https://api.slack.com/types/group)
        """
        return self.slackClient.api_call('groups.list')['groups']

    def mpim_list(self):
        """
        Retorna uma lista com todos os chats (conversas multiusuario) que o usuario participa.
        Cada item da lista e um dicionario com os detalhes de cada chat.
        (para detalhes sobre o dicionario de retorno veja https://api.slack.com/types/mpim)
        """
        return self.slackClient.api_call('mpim.list')['groups']

    def im_list(self):
        """
        Retorna uma lista com todas as "Direct Messages" do usuario.
        Cada item da lista e um dicionario com os detalhes de cada conversa.
        (para detalhes sobre o dicionario de retorno veja https://api.slack.com/types/im)
        """
        return self.slackClient.api_call('im.list')['ims']

    def user_list(self):
        """
        Retorna uma lista com todos os usuario de time.
        Cada item da lista e um dicionario com os detalhes de cada usuario
        (para detalhes sobre o dicionario de retorno veja https://api.slack.com/types/user)
        """
        return self.slackClient.api_call('users.list')['members']

    def channel_members(self, channel_id):
        """
        Retorna uma lista com os IDs dos membros do canal
        (para mais informacoes veja https://api.slack.com/methods/channels.info)
        :param channel_id: Id do canal do qual quer obter a lista de membros
        :return: Lista de IDs dos membros do canal
        """
        result = self.slackClient.api_call('channels.info', channel=channel_id)
        if result['ok']:
            return result['channel']['members']

        result = self.slackClient.api_call('groups.info', channel=channel_id)
        if result['ok']:
            return result['group']['members']
