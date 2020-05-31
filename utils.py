from botcore import Plugin, Bot

class MessageResponseBasePlugin(Plugin):
    PLUGIN_NAME = "Message-Response"

    def handle_message(self, msgchain, sender, msgtype, event):
        """
        Handles group/temp/friend messages in a uniform way.

        Other events can be handled by implementing `handle_xxx(self, event)` methods,
          where `xxx` is the type of the event, in UpperCamelCase.
        """
        raise NotImplementedError

    def handle_event(self, event):
        if "messageChain" in event:
            return self.handle_message(event["messageChain"], event["sender"], event["type"], event)
        else:
            return getattr(self, 'handle_' + event["type"], lambda _:None)(event)

    def reply(self, event, msg=None, quote=True, notify=False, private=False, ban_duration=0, revoke=False):
        if event["type"] == "GroupMessage" and not private:
            if msg is not None:
                if notify:
                    msg = [
                            {
                                "type": "At",
                                "target": event["sender"]["id"]
                            }
                        ] + msg
                if quote:
                    self.post_sendGroupMessage(
                      target=event["sender"]["group"]["id"],
                      quote=event["messageChain"][0]["id"],
                      messageChain=msg)
                else:
                    self.post_sendGroupMessage(
                      target=event["sender"]["group"]["id"],
                      messageChain=msg)
            if ban_duration > 0:
                self.post_mute(target=event["sender"]["group"]["id"], memberId=event["sender"]["id"], time=ban_duration)
            if revoke:
                self.post_recall(target=event["messageChain"][0]["id"])
        elif event["type"] == "FriendMessage":
            if msg is not None:
                if quote:
                    self.post_sendFriendMessage(
                      target=event["sender"]["id"],
                      quote=event["messageChain"][0]["id"],
                      messageChain=msg)
                else:
                    self.post_sendFriendMessage(
                      target=event["sender"]["id"],
                      messageChain=msg)
        elif event["type"] == "TempMessage" or private:
            if msg is not None:
                if quote:
                    self.post_sendTempMessage(
                      qq=event["sender"]["id"],
                      group=event["sender"]["group"]["id"],
                      quote=event["messageChain"][0]["id"],
                      messageChain=msg)
                else:
                    self.post_sendTempMessage(
                      qq=event["sender"]["id"],
                      group=event["sender"]["group"]["id"],
                      messageChain=msg)

    def __getattr__(self, attr):
        if attr[:4] == "get_":
            def getf(**kwargs):
                self.bot.get("/" + attr[4:], kwargs)
            return getf
        elif attr[:5] == "post_":
            def postf(**kwargs):
                self.bot.post("/" + attr[5:], kwargs)
            return postf
        else:
            raise AttributeError(attr)
