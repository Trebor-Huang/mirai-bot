from botcore import Plugin

class PingPlugin(Plugin):
    PLUGIN_NAME = "Ping"
    def handle_event(self, event):
        if "messageChain" in event:
            for c in event["messageChain"]:
                if c["type"] == "At":
                    if c["target"] == self.bot.bot_qq:
                        if event["type"] == "GroupMessage":
                            self.bot.post("/sendGroupMessage",
                                    {
                                        "target": event["sender"]["group"]["id"],
                                        "messageChain": [
                                            {
                                                "type": "Plain",
                                                "text": "PONG"
                                            }
                                        ]
                                    }
                                )
                        elif event["type"] == "FriendMessage":
                            self.bot.post("/sendFriendMessage", 
                                    {
                                        "target": event["sender"]["id"],
                                        "messageChain": [
                                            {
                                                "type": "Plain",
                                                "text": "PONG"
                                            }
                                        ]
                                    }
                                )
                        elif event["type"] == "GroupMessage":
                            self.bot.post("/sendGroupMessage", 
                                    {
                                        "target": event["sender"]["group"]["id"],
                                        "messageChain": [
                                            {
                                                "type": "Plain",
                                                "text": "PONG"
                                            }
                                        ]
                                    }
                                )
                        self.logger.info("PONG")
                        return False
        return True

plugins = [(0, PingPlugin)]
