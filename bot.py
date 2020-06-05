import botcore, sys, pathlib, importlib, logging

logging.basicConfig(format="[%(levelname)s] %(name)s \t- %(message)s")

plugins_path = pathlib.Path(__file__).parent.absolute().glob('plugins/*.py')
plugins_modules = [importlib.import_module("plugins." + pp.stem) for pp in plugins_path]
plugins_list = sorted([p for m in plugins_modules if hasattr(m, "plugins") for p in m.plugins], reverse=True)

bot = botcore.Bot(int(sys.argv[1]), auth_key=sys.argv[2], plugins=[p for i, p in plugins_list])
bot.connect()
while input() != "stop":
    pass
bot.disconnect()
