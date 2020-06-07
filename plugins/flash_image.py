from utils import plain
from plugin import MessageResponseBasePlugin

class FlashImagePlugin(MessageResponseBasePlugin):
    PLUGIN_NAME = "Flash"
    HELP_MESSAGE = (
        "闪照捕捉功能。在任何人发送闪照的时候，返回闪照链接。"
        "本功能仅为测试用途。计划在不久后删除这个功能，或者添加开关。"
    )

    def handle_message(self, msgchain, sender, msgtype, event):
        for c in msgchain:
            if c["type"] == "FlashImage":
                self.logger.info("Flash image detected in %s by %s" % (msgtype, sender))
                self.reply(event, msg=plain(c["url"]), quote=False, notify=True)
        return True

plugins = [(10000, FlashImagePlugin)]

