# 打包发布

```bash
pyinstaller -D --name "MyTranslator" -w --hidden-import=queue -i res/translate.ico main.py
```