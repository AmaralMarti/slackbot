# coding=utf-8

from threading import Thread
import datetime as dt


class SlackBotInfo(Thread):
    def __init__(self, slackbot):
        Thread.__init__(self)
        self.__bot = slackbot

        self.__user_list = dict()
        self.__channel_list = dict()
        self.__group_list = dict()
        self.__mpim_list = dict()
        self.__im_list = dict()

        self.active = False

        self.updating_user_list = False
        self.updating_channel_list = False
        self.updating_group_list = False
        self.updating_mpim_list = False
        self.updating_im_list = False

    def run(self):
        self.active = True
        while self.active:
            ini = dt.datetime.now()

            self.__user_list = self.__get_user_list()
            self.__channel_list = self.__get_channel_list()
            self.__group_list = self.__get_group_list()
            self.__mpim_list = self.__get_mpim_list()
            self.__im_list = self.__get_im_list()

            # atualiza as listas a cada 60 segundos, mas de forma que o looping
            # pode ser interrompido instantaneamente se for desativado
            while (dt.datetime.now() - ini).total_seconds() < 60:
                if not self.active:
                    break

    def get_user_info(self, id_user):
        result = dict()
        result['ok'] = False
        result['id'] = id_user

        if self.updating_user_list:
            while self.updating_user_list:
                pass
        if id_user in self.__user_list.keys():
            result['name'] = self.__user_list[id_user]
            result['ok'] = True

        return result

    def get_channel_info(self, id_channel):
        result = dict()
        result['ok'] = False
        result['id'] = id_channel

        # IM
        if self.updating_im_list:
            while self.updating_im_list:
                pass
        if id_channel in self.__im_list.keys():
            result['name'] = self.get_user_info(self.__im_list[id_channel])['name']
            result['type'] = 'im'
            result['ok'] = True
            return result

        # MPIM
        if self.updating_mpim_list:
            while self.updating_mpim_list:
                pass
        if id_channel in self.__mpim_list.keys():
            result['name'] = self.__mpim_list[id_channel]
            result['type'] = 'mpim'
            result['ok'] = True
            return result

        # GROUP
        if self.updating_group_list:
            while self.updating_group_list:
                pass
        if id_channel in self.__group_list.keys():
            result['name'] = self.__group_list[id_channel]
            result['type'] = 'group'
            result['ok'] = True
            return result

        # CHANNEL
        if self.updating_channel_list:
            while self.updating_channel_list:
                pass
        if id_channel in self.__channel_list.keys():
            result['name'] = self.__channel_list[id_channel]
            result['type'] = 'channel'
            result['ok'] = True
            return result

        return result

    def __get_user_list(self):
        self.updating_user_list = True
        try:
            result = dict()
            user_list = self.__bot.user_list()
            for user in user_list:
                result[user['id']] = user['name']
            return result
        finally:
            self.updating_user_list = False

    def __get_channel_list(self):
        self.updating_channel_list = True
        try:
            result = dict()
            channel_list = self.__bot.channel_list()
            for channel in channel_list:
                result[channel['id']] = channel['name']
            return result
        finally:
            self.updating_channel_list = False

    def __get_group_list(self):
        self.updating_group_list = True
        try:
            result = dict()
            group_list = self.__bot.group_list()
            for group in group_list:
                result[group['id']] = group['name']
            return result
        finally:
            self.updating_group_list = False

    def __get_mpim_list(self):
        self.updating_mpim_list = True
        try:
            result = dict()
            mpim_list = self.__bot.mpim_list()
            for mpim in mpim_list:
                result[mpim['id']] = mpim['name']
            return result
        finally:
            self.updating_mpim_list = False

    def __get_im_list(self):
        self.updating_im_list = True
        try:
            result = dict()
            im_list = self.__bot.im_list()
            for im in im_list:
                result[im['id']] = im['user']
            return result
        finally:
            self.updating_im_list = False
