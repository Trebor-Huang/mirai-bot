from utils import plain
from plugin import MessageResponseBasePlugin

class PingPlugin(MessageResponseBasePlugin):
    PLUGIN_NAME = "Ping"
    HELP_MESSAGE = "在任何群聊中@bot。如果bot处于开机状态，则会回复PONG。"

    def handle_message(self, msgchain, sender, msgtype, event):
        for c in msgchain:
            if c["type"] == "At" and c["target"] == self.bot.bot_qq:
                self.logger.info("PONG from %s" % (sender["id"]))
                self.reply(event, msg=plain("PONG"))
                return False
        return True

plugins = [(0, PingPlugin)]

