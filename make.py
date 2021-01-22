mode = "release"

if __name__ == '__main__':
    from PyInstaller.__main__ import run
    if mode == "debug":
        opts = ['main.py', '-i', './res/translate.ico', '--debug', 'all', '-n', 'MyTranslator']
    else:
        opts = ['main.py', '-i', './res/translate.ico', '-w', '-n', 'MyTranslator']
    run(opts)