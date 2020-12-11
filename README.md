# 打包发布

```bash
pyinstaller --clean -D --name "MyTranslator" -w --hidden-import=queue -i res/translate.ico main.py –exclude-module Qt5Quick
```