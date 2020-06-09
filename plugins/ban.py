import utils, plugin

class BanPlugin(plugin.CommandPlugin):
    PLUGIN_NAME = "Ban"
    COMMAND_NAME = ["ban"]
    ADMIN = True
    HELP_MESSAGE = "禁言。"
    USAGE = [
        (plugin.COMMAND_PREFIX + "ban @群成员 时间","时间以秒为单位，0为解除禁言。")
    ]

    def handle_command(self, cmd, text, sender, msgtype, event):
        if sender["id"] not in self.bot.admins:
            return
        if msgtype == "GroupMessage":
            if text.strip() == "":
                if len(event["messageChain"]) == 4:
                    if event["messageChain"][2]["type"] == "At":
                        if event["messageChain"][3]["type"] == "Plain":
                            try:
                                t = int(event["messageChain"][3]["text"].strip())
                            except ValueError as e:
                                self.reply(event, "格式错误。")
                                return
                            try:
                                self.post_mute(target=event["sender"]["group"]["id"], memberId=event["messageChain"][2]["target"], time=t)
                                return
                            except RuntimeError as e:
                                st = e.args[0]
                                if st["code"] == 10:
                                    self.reply(event, "无权操作。")
                                    return
                                else:
                                    raise e
            self.reply(event, "格式错误。")

plugins = [(1000, BanPlugin)]
