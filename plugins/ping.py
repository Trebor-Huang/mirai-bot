from utils import MessageResponseBasePlugin

class PingPlugin(MessageResponseBasePlugin):
    PLUGIN_NAME = "Ping"

    def handle_message(self, msgchain, sender, msgtype, event):
        for c in msgchain:
            if c["type"] == "At" and c["target"] == self.bot.bot_qq:
                self.reply(event, msg=[
                        {
                            "type": "Plain",
                            "text": "PONG"
                        }
                    ])
                return True
        return False


plugins = [(0, PingPlugin)]
