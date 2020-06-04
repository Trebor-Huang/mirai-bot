from utils import MessageResponseBasePlugin, plain

class FlashImagePlugin(MessageResponseBasePlugin):
    PLUGIN_NAME = "Flash"

    def handle_message(self, msgchain, sender, msgtype, event):
        for c in msgchain:
            if c["type"] == "FlashImage":
                self.reply(event, msg=plain(c["url"]), quote=False, notify=True)
        return True

plugins = [(10000, FlashImagePlugin)]

