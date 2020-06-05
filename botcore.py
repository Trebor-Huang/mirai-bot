"""
Core functionalities of the bot.

Accepts plugins from the `plugins/` folder.
"""

import requests, logging, threading, time, json

logger = logging.getLogger("Core")
logger.setLevel("INFO")

class MessageFetcher(threading.Thread):
    def __init__(self, bot):
        super(MessageFetcher, self).__init__()
        self.bot = bot
        self.running = False

    def run(self):
        try:
            self.running = True
            while self.running:
                rs = self.bot.get("/fetchMessage", {"count": "10"})
                self.bot.event_queue.extend(rs["data"])
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass

class PluginRunner(threading.Thread):
    def __init__(self, bot):
        super(PluginRunner, self).__init__()
        self.bot = bot
        self.running = False

    def process(self, event):
        for p in self.bot.plugins:
            if not p.handle_event(event):
                break

    def run(self):
        try:
            self.running = True
            while self.running:
                if self.bot.event_queue:
                    e = self.bot.event_queue.pop(0)
                    threading.Thread(target=self.process, args=(e,)).start()
                else:
                    time.sleep(0.01)
        except KeyboardInterrupt:
            pass


class Bot:
    def __init__(self, bot_qq, api_url="http://localhost:8080", auth_key="", plugins=None):
        logger.info("Checking for mirai server...")
        mirai_status = requests.get(api_url + "/about").json()
        if mirai_status["code"] != 0:
            raise RuntimeError(mirai_status)
        logger.info("Mirai HTTP version: %s" % mirai_status["data"]["version"])
        self.auth_key = auth_key
        self.api_url = api_url
        self.plugins_class = [] if plugins is None else plugins
        self.bot_qq = bot_qq

    def connect(self):
        auth_status = requests.post(self.api_url + "/auth", data=json.dumps({"authKey": self.auth_key})).json()
        if auth_status["code"] == 1:
            raise ValueError("Invalid auth key.")
        self.session = auth_status["session"]
        logger.info("Session acquired: %s" % self.session)
        verify_status = self.post("/verify", {"qq": self.bot_qq})
        # success, start fetcher thread
        self.event_queue = []
        self.fetcher = MessageFetcher(self)
        self.fetcher.start()
        # initialize plugins
        self.plugins = []
        for c in self.plugins_class:
            logger.info("Loading %s" % c.PLUGIN_NAME)
            self.plugins.append(c(self))
        self.plugin_runner = PluginRunner(self)
        self.plugin_runner.start()

    def post(self, api, data):
        d = {i : data[i] for i in data}
        d["sessionKey"] = self.session
        status = requests.post(self.api_url + api, data=json.dumps(d)).json()
        if status["code"] != 0:
            raise RuntimeError(status)
        return status

    def get(self, api, params):
        d = {i : params[i] for i in params}
        d["sessionKey"] = self.session
        status = requests.get(self.api_url + api, params=d).json()
        if status["code"] != 0:
            raise RuntimeError(status)
        return status

    def disconnect(self):
        for p in self.plugins:
            logger.info("Disconnecting %s" % p.PLUGIN_NAME)
            p.handle_disconnect()
        logger.info("Shutting down plugin driver")
        self.plugin_runner.running = False
        self.plugin_runner.join()
        logger.info("Stopping event polling loop")
        self.fetcher.running = False
        self.fetcher.join()
        logger.info("Releasing session")
        self.post("/release", {"qq": self.bot_qq})
        logger.info("Disconnected")

class Plugin:
    PLUGIN_NAME = "Base"
    def __init__(self, bot):
        self.bot = bot  # run when loading plugins
        self.logger = logging.getLogger(self.PLUGIN_NAME)
        self.logger.setLevel("INFO")

    def handle_event(self, event):
        return True  # if False, block execution of next plugin

    def handle_disconnect(self):
        return

class ExamplePlugin(Plugin):
    PLUGIN_NAME = "Example"
    def __init__(self, bot):
        super().__init__(bot)
        self.logger.info("Starting Example Plugin")

    def handle_event(self, event):
        self.logger.info(event)
        return True

    def handle_disconnect(self):
        self.logger.info("Example Plugin disconnecting")
