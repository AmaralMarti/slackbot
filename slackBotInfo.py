# coding=utf-8

from threading import Thread
import time
import datetime as dt


class slackBotInfo(Thread):
    def __init__(self, slackBot):
        Thread.__init__(self)
        self.__bot = slackBot

        self.__userList = dict()
        self.__channelList = dict()
        self.__groupList = dict()
        self.__mpimList = dict()
        self.__imList = dict()

        self.active = False

        self.updatingUserList = False
        self.updatingChannelList = False
        self.updatingGroupList = False
        self.updatingMpimList = False
        self.updatingImList = False

    def run(self):
        self.active = True
        while self.active:
            ini = dt.datetime.now()

            self.__userList = self.__getuserlist()
            self.__channelList = self.__getchannellist()
            self.__groupList = self.__getgrouplist()
            self.__mpimList = self.__getmpimlist()
            self.__imList = self.__getimlist()

            while (dt.datetime.now() - ini).total_seconds() < 60:
                if not self.active:
                    break

    def getUseInfo(self, id):
        result = dict()
        result['ok'] = False
        result['id'] = id

        if self.updatingUserList:
            while self.updatingUserList:
                pass
        if id in self.__userList.keys():
            result['name'] = self.__userList[id]
            result['ok'] = True

        return result

    def getChannelInfo(self, id):
        result = dict()
        result['ok'] = False
        result['id'] = id

        # IM
        if self.updatingImList:
            while self.updatingImList:
                pass
        if id in self.__imList.keys():
            result['name'] = self.getUseInfo(self.__imList[id])['name']
            result['type'] = 'im'
            result['ok'] = True
            return result

        # MPIM
        if self.updatingMpimList:
            while self.updatingMpimList:
                pass
        if id in self.__mpimList.keys():
            result['name'] = self.__mpimList[id]
            result['type'] = 'mpim'
            result['ok'] = True
            return result

        # GROUP
        if self.updatingGroupList:
            while self.updatingGroupList:
                pass
        if id in self.__groupList.keys():
            result['name'] = self.__groupList[id]
            result['type'] = 'group'
            result['ok'] = True
            return result

        # CHANNEL
        if self.updatingChannelList:
            while self.updatingChannelList:
                pass
        if id in self.__channelList.keys():
            result['name'] = self.__channelList[id]
            result['type'] = 'channel'
            result['ok'] = True
            return result

        return result

    def __getuserlist(self):
        self.updatingUserList = True
        try:
            result = dict()
            userlist = self.__bot.userList()
            for user in userlist:
                result[user['id']] = user['name']
            return result
        finally:
            self.updatingUserList = False

    def __getchannellist(self):
        self.updatingChannelList = True
        try:
            result = dict()
            channellist = self.__bot.channelList()
            for channel in channellist:
                result[channel['id']] = channel['name']
            return result
        finally:
            self.updatingChannelList = False

    def __getgrouplist(self):
        self.updatingGroupList = True
        try:
            result = dict()
            grouplist = self.__bot.groupList()
            for group in grouplist:
                result[group['id']] = group['name']
            return result
        finally:
            self.updatingGroupList = False

    def __getmpimlist(self):
        self.updatingMpimList = True
        try:
            result = dict()
            mpimlist = self.__bot.mpimList()
            for mpim in mpimlist:
                result[mpim['id']] = mpim['name']
            return result
        finally:
            self.updatingMpimList = False

    def __getimlist(self):
        self.updatingImList = True
        try:
            result = dict()
            imlist = self.__bot.imList()
            for im in imlist:
                result[im['id']] = im['user']
            return result
        finally:
            self.updatingImList = False
