# QQ Bot

The code of my qq bot!

- [QQ Bot](#qq-bot)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [How it works](#how-it-works)
    - [Mirai Basics](#mirai-basics)
    - [Bot structure](#bot-structure)
  - [Plugins](#plugins)
    - [Plugin Basics](#plugin-basics)
    - [The Message-Response Plugin Framework](#the-message-response-plugin-framework)

Currently it has the ability to:
- recover the link to flash images (this is offensive, it will be turned off by default when I finished debugging it).
- answer pings.

## Requirements

You need Python 3.5+ to run the bot. (Older versions may be able to run the bot, but it is not tested.) To use [mirai](https://github.com/mamoe/mirai), you need appropriate versions of Java.

## Usage

Set up a Mirai server as instructed [here](https://github.com/mamoe/mirai), possibly with the [wrapper](https://github.com/mamoe/mirai-console-wrapper). And install the [HTTP API plugin](https://github.com/mamoe/mirai-api-http). Remember to modify the auth key of the HTTP API plugin. Start the bot by `python3 ./bot.py <YOUR-BOT-QQ> <YOUR-HTTP-API-AUTH-KEY>`. Stop it by entering `stop`.

## How it works

### Mirai Basics

TODO

### Bot structure

The bot has two threads to fetch events (every 0.5 seconds) and run plugins, respectively. The `post(api, data)` and `get(api, params)` method access the [APIs provided by mirai HTTP](https://github.com/mamoe/mirai-api-http), and handles session authorizing.

## Plugins

### Plugin Basics

The bot accepts plugins in the `./plugins` folder.

A plugin file is a python source file containing a list `plugins` of tuples `(level, PluginClass)`, where `PluginClass` is a child class of `Plugin`. It should contain a class attribute `PLUGIN_NAME`, for logging purposes.

The `handle_event(self, event)` and `handle_disconnect(self)` methods handle QQ events and clean up the plugin for disconnecting, respectively. Events are handled by each plugin, where plugins with higher `level` gets the event first. If `handle_event` returns `False`, the event is not handed down to the subsequent plugins. This means that if a plugin hangs, subsequent plugins cannot handle that event.

You can use `self.bot` to access the `Bot` object, and `self.logger` to access the logger.

### The Message-Response Plugin Framework

To more effectively develop plugins, you can inherit from the `utils.MessageResponseBasePlugin` class. Then you can handle messages (from friends, groups or temporary messages) by reimplementing the `handle_message(self, msgchain, sender, msgtype, event)` function. Other events can be processed with `handle_EventType(self, event)` methods, where the types of the event are listed [here](https://github.com/mamoe/mirai-api-http/blob/master/EventType.md).

You can invoke `self.reply(event, msg=None, quote=True, notify=False, private=False, ban_duration=0, revoke=False)` to more effectively reply to messages (currently non-message events are ignored by this method).
- If `msg` is not `None`, the bot replies to the message referred by `event` with the message chain `msg`. And you can quote or "at" (i.e. notify with the `@` construct in QQ) the sender by setting the corresponding flags; these flags are ignored if they are not available. You may also send private messages (as opposed to group messages, e.g. to avoid cluttering) by setting the `private` flag.
- If `ban_duration > 0`, the sender will be banned for `ban_duration` seconds, which cannot exceed 30 days. If the bot has no priviledge to do this it raises a `RuntimeError`.
- If `revoke` is set to `True`, the message `event` is revoked if possible. If the bot has no priviledge to do this it raises a `RuntimeError`.

`self.get_xxx` and `self.post_xxx` (with keyword arguments) sends the corresponding requests to the HTTP API, listed [here](https://github.com/mamoe/mirai-api-http).
