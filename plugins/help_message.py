import utils, plugin

class HelpPlugin(plugin.CommandPlugin):
    """
    Displays help messages.

    If a plugin has attribute `HELP_MESSAGE`, it is displayed
      when the command `help` is called.

    If additionally there is an attribute `USAGE`, consisting of
      a list of tuples `(usage, explanation)`, it is also shown.

    Example:
    Help
        显示这个帮助
        使用示例：
          > help
    """

    PLUGIN_NAME = "Help"
    COMMAND_NAME = ["help"]
    HELP_MESSAGE = "显示这个帮助。"
    USAGE = [
        (plugin.COMMAND_PREFIX + "help","")
    ]

    def handle_command(self, cmd, text, sender, msgtype, event):
        for p in self.bot.plugins:
            hm = ""
            if hasattr(p, "HELP_MESSAGE"):
                hm += p.PLUGIN_NAME + "\n"
                for l in p.HELP_MESSAGE.split("\n"):
                    hm += "    " + l + "\n"
                if hasattr(p, "USAGE"):
                    hm += "\n    使用示例："
                    for usage, explanation in p.USAGE:
                        hm += "      " + usage
                        for l in explanation.split("\n"):
                            if l != "":
                                hm += "      " + l + "\n"
                        hm += "\n"
                self.reply(event, hm.strip(), quote=False, private=True)
        self.reply(event, "帮助已发送至私聊。")

plugins = [(1000, HelpPlugin)]