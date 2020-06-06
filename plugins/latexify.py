import os, hashlib, utils, plugin, time

def get_preamble(usepackage=(), definitions=""):
    usepackage += ("amssymb", "amsmath", "amsfonts")
    return r"\documentclass[varwidth,border=2pt]{standalone}" + \
      "\n\\usepackage{" + ", ".join(usepackage) + "}\n\\usepackage{xeCJK}\n" + definitions + "\n\\begin{document}\n"

def get_source(source, usepackage=(), definitions=""):
    return get_preamble(usepackage, definitions) + source + "\n\\end{document}\n"

def compile_latex(src):
    u = hashlib.sha256(src.encode('utf-8')).hexdigest()
    if not os.path.isfile("../plugins/MiraiAPIHTTP/images/%s.jpeg" % u):
        with open("./resources/latex/%s.tex" % u, "w") as f:
            f.write(src)
        # TODO write up explanations
        compile_return = os.system('bash -c "ulimit -t 30 ; ( docker run -m 1GB -v $(pwd)/resources/latex/%s.tex:/home/latex/texput.tex --name latex_container%s treborhuang/latex > /dev/null ) 2> >(grep -v \'Your kernel does not support swap limit capabilities\' >&2)"' % (u, u))
        if compile_return == 137:  # timed out
            return ("Timeout", (), "")
        copy_return = os.system("docker cp latex_container%s:/home/latex/ ./resources/latex/%s/" % (u, u))
        os.system("docker container rm latex_container%s > /dev/null" % u)
        if compile_return != 0:
            with open("./resources/latex/%s/texput.log" % u, "r") as f:
                logs = f.read()
            error_log = logs[logs.find("\n!"):logs.find("Here is how much of")]
            if error_log:
                return ("Failed", (compile_return, copy_return), error_log.strip())
            return ("Failed-NoError", (compile_return, copy_return), logs)
        convert_return = os.system("convert -density 500 ./resources/latex/%s/texput.pdf ./resources/latex/%s.jpeg" % (u, u))
        resize_return = os.system("convert ./resources/latex/%s.jpeg -resample 400 ../plugins/MiraiAPIHTTP/images/%s.jpeg" % (u, u))
        if convert_return or resize_return:
            return ("Failed", (compile_return, copy_return, convert_return, resize_return), "请告诉我的主人：" + str(((compile_return, copy_return, convert_return, resize_return))))
    else:
        return ("Cached", (), u + ".jpeg")
    return ("Done", (compile_return, copy_return, convert_return, resize_return), u + ".jpeg")

class LaTeXifyPlugin(plugin.CommandPlugin):
    PLUGIN_NAME = "LaTeX"
    COMMAND_NAME = ["render", "latex"]

    def render(self, src, ismath, event):
        task_ns = hex(hash(time.time()))[8:]
        self.logger.info("Received LaTeX task @ %s" % task_ns)
        pkgs = ()
        defs = ""
        try:
            if src[:22] == "\\begin{bot-usepackage}":
                src = src[22:]
                pkg, src = src.split("\\end{bot-usepackage}")
                pkgs = tuple(pkg.split())
            if src[:16] == "\\begin{bot-defs}":
                src = src[16:]
                defs, src = src.split("\\end{bot-defs}")
        except Exception as e:
            self.reply(event, utils.plain("格式不正确"))
            return
        if ismath:
            src = "$ \\displaystyle " + src + "$"
        src_ltx = get_source(src, pkgs, defs)
        r, rets, l = compile_latex(src_ltx)
        self.logger.info("Task %s %s: " % (task_ns, r) + str(rets))
        try:
            if r == "Timeout":
                self.reply(event, utils.plain("TLE~qwq"))
            elif r == "Failed":
                self.reply(event, utils.plain("出错了qaq"))
                self.reply(event, utils.plain(utils.clamp(l, 5000)), private=True)
            elif r == "Failed-NoError":
                self.reply(event, "出错了qaq，而且很不寻常，跟我主人说吧qwq")
            elif r in ["Done", "Cached"]:
                self.reply(event, [{"type": "Image", "path": l}])
        except Exception as e:
            self.logger.exception(e)
            self.reply(event, "似乎你（或者群主设置）不允许群内陌生人私聊，或者网络错误："+str(e)+"请将错误代码和发生的时间告诉我的主人", quote=False, notify=True)

    def handle_command(self, cmd, text, sender, msgtype, event):
        self.render(text, cmd=="latex", event)

plugins = [(1000, LaTeXifyPlugin)]

if __name__ == "__main__":
    src_test = get_source("$ a^2 + b^2 $")
    compile_latex(src_test)
