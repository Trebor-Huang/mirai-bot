from utils import plain
from plugins import MessageResponseBasePlugin

class PingPlugin(MessageResponseBasePlugin):
    PLUGIN_NAME = "Ping"

    def handle_message(self, msgchain, sender, msgtype, event):
        for c in msgchain:
            if c["type"] == "At" and c["target"] == self.bot.bot_qq:
                self.logger.info("PONG from %s" % (sender["id"]))
                self.reply(event, msg=plain("PONG"))
                return False
        return True

plugins = [(0, PingPlugin)]

