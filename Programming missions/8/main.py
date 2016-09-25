#!/usr/bin/env python2
# coding: utf8

import irclib
import ircbot
from time import gmtime, strftime
import re
import hashlib
import config

HOST = "irc-hub.hackthissite.org"
PORT = 6667

step1_canal = "#perm8"
step3_canal = "#takeoverz"

class BotModeration(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(HOST, PORT)],
                                           config.USER, config.USER+" (Programming challenge #8)")
        print("démarré")

    def on_nicknameinuse(self, c, e):
        self.log_irc('on_nicknameinuse', c, e)
        c.nick(c.get_nickname() + "_")

    def on_dccmsg(self, c, e):
        self.log_irc('on_dccmsg', c, e)

    def on_start(self, c, e):
        self.log_irc('on_start', c, e)

    def on_welcome(self, c, e):
        self.log_irc('on_welcome', c, e)
        c.join(step1_canal)

    def on_join(self, c, e):
        self.log_irc('on_join', c, e)

        channel = e.target()
        if channel == step1_canal:
            self.step0_identification(c)
        elif channel == step3_canal:
            self.step3_attack(c)

    def on_pubmsg(self, c, e):
        self.log_irc('on_pubmsg', c, e)

    def on_privmsg(self, c, e):
        self.log_irc('on_privmsg', c, e)

    def on_pubnotice(self, c, e):
        self.log_irc('on_pubnotice', c, e)

    def on_privnotice(self, c, e):
        self.log_irc('on_privnotice', c, e)
        auteur,message= self.irc(c, e)
        if auteur=='NickServ' and message=='Password accepted - you are now recognized.':
            self.step1_notice_moo(c)
        elif auteur == 'moo':
            string = self.step2_get_string(message)
            if len(string) > 0:
                self.step2_hash_moo(string, c)
            else:
                if message == '!perm8-attack':
                    self.step3_join(c);

    def step0_identification(self, c):
        self.privmsg(c, 'NickServ', 'IDENTIFY '+config.MDP)

    def step1_notice_moo(self, c):
        self.notice(c, 'moo', '!perm8')

    # retourne le groupe de la regex
    def step2_get_string(self, message):
        regex = "md5 (.+)"
        string = ''
        for match in re.finditer(regex, message):
            string = match.group(1)
        return string

    def step2_hash_moo(self, string, c):
        string = string.encode('utf-8')
        md5 = hashlib.md5(string).hexdigest()
        message = '!perm8-result '+md5
        self.notice(c, 'moo', message)

    def step3_join(self, c):
        c.join(step3_canal)

    def step3_attack(self, c):
        print("ATTACK")
        c.kick(step3_canal, 'moo', 'prog/ level 8')

    def on_mode(self, c, e):
        self.log_irc('on_mode', c, e)

    def on_kick(self, c, e):
        self.log_irc('on_kick', c, e)

    # retourn un tuple (auteur, message)
    def irc(self, c, e):
        auteur = irclib.nm_to_n(e.source())
        if len(e.arguments()) > 0:
            message = e.arguments()[0]
        else:
            message = '(null)'
        return auteur, message

    # log une action IRC
    def log_irc(self, tag, c, e):
        auteur, message = self.irc(c, e)
        self.log(tag, auteur+' : '+message)

    # log
    def log(self, tag, message):
        print('['+strftime("%H:%M:%S", gmtime())+'] '+'('+tag+') '+message)

    def notice(self, c, destinataire, message):
        self.log('send notice', destinataire+" : "+message)
        c.notice(destinataire, message)

    def privmsg(self, c, destinataire, message):
        self.log('send privmsg', destinataire+" : "+message)
        c.privmsg(destinataire, message)

import inspect

if __name__ == "__main__":
    print("démarrage...")
    bot = BotModeration()
    # toutes les méthodes de ircbot.SingleServerIRCBot
    # for methode in inspect.getmembers(bot, predicate=inspect.ismethod):
    #     print(methode)
    bot.start()
