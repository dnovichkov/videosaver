Работает все это с третьей версией Python.

Рекомендуется настроить виртуальное окружение. Вот "правильные" ссылки:
[https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html) и 
[https://virtualenv.pypa.io/en/stable/userguide/](https://docs.python.org/3/library/venv.html)
На своей Win-машине я сделал это так:

```
python -m venv env
call env/scripts/activate.bat
```

После этого устанавливаем необходимые модули

```
pip install -r requirements.txt
```

Для скачивания аудиодорожек необходимо иметь установленный в системе ffmpeg.