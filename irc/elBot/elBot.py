"""
Copyright Ian O'Hara 2012
Available under GPL V2.0

elBot - An IRC bot written for the heck of it
"""

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys

# imports for the fun stuff
from ElBotTrie import ElBotTrie

class MessageLogger:
    def __init__(self, file):
        self.file = file

    def log(self, message):
        timestamp = time.strftime("[%H:%M:%S]", time.localtime(time.time()))
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

class WordCounter():
    def __init__(self, user_file='user_wordcounts.csv'):
        self.user_tries = {}
        self.user_file = user_file
        self.load_users(user_file)

    def load_users(self, filename):
        f = open(filename)
        try:
            for line in f:
                (user, word, count) = line.split(',')[0:3]
                self.add_sentence(user.translate(None, ' '), (' ' + word) * int(count))
        finally:
            f.close()

    def write_users(self, filename=None):
        if not filename:
            filename = self.user_file

        f = open(filename, 'w')
        try:
            for user in self.user_tries.keys():
                this_words = self.user_tries[user].get_word_dict()
                for (word, count) in this_words.iteritems():
                    f.write('%s,%s,%d\n' % (user, word, count))
        finally:
            f.close()

    def add_sentence(self, user, sentence):
        if not self.user_tries.has_key(user):
            self.user_tries[user] = ElBotTrie()
        self.user_tries[user].add_sentence(sentence)

    def get_count(self, user):
        if self.user_tries.has_key(user):
            return self.user_tries[user].total_words()
        else:
            return 0

    def get_word_count(self, user, word):
        if self.user_tries.has_key(user):
            return self.user_tries[user].count(word)
        else:
            return 0

class ElBot(irc.IRCClient):
    nickname = "elBot_testing"
    def __init__(self):
        self.word_counter = WordCounter()
        """
        A dict where the keys are commands (!<command> from user)
        and the values are functions to call when a command is executed.
           The functions must have the signature:
             func(self, channel=str(), user=str(), *args) 
        """
        self.commands = dict()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger(open(self.factory.filename, "a"))
        self.logger.log("[connected at %s]" % 
                        time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("[disconnected at %s]" % 
                        time.asctime(time.localtime(time.time())))
        self.logger.close()
        self.word_counter.write_users()

    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("[I have joined %s]" % channel)

    def privmsg(self, user, channel, msg):
        """This gets called when the bot receives a message."""
        user = user.split('!', 1)[0]
        self.logger.log("<%s> %s" % (user, msg))
        
        self.word_counter.add_sentence(user,msg)

        if self.nickname in msg:
            self.say(channel, 'What\'s that, ya hosier?')

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = 'Afraid I\'m pretty much a skeleton right now, so private messages don\'t lead to anything fun.' 
            self.msg(user, msg)
            return
        
        msg_components = msg.split(' ')
        command = msg_components[0]
        if '!wc' in command:
            wc_user = user
            if len(msg_components) > 1:
                wc_user = msg_components[1]
            print 'Someone asked for a wordcount for user %s.' % wc_user
            user_wc = self.word_counter.get_count(wc_user)
            self.say(channel, '%s has said %d words.' % (wc_user, user_wc))
        elif '!write_wc' in command:
            self.word_counter.write_users()

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.logger.log("* %s %s" % (user, msg))

    # irc callbacks

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        self.logger.log("%s is now known as %s" % (old_nick, new_nick))

class ElBotFactory(protocol.ClientFactory):

    def __init__(self, channel=None, filename=None, settings=None):
        self.channel = channel
        self.filename = filename
        self.settings = settings

    def buildProtocol(self, addr):
        p = ElBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # initialize logging
    log.startLogging(sys.stdout)
    
    # create factory protocol and application
    botFactory = ElBotFactory('#Eng_Bestiary', 'example_logger.txt')

    # connect factory to this host and port
    reactor.connectTCP("ec2-107-20-56-124.compute-1.amazonaws.com", 6667, botFactory)

    # run bot
    reactor.run()
