# vkbot
Этот проект является простейшей реализацией бота для группы вконтакте, который отвечает на первое сообщения пользователя, игнорируя все последующие, кроме фотографий, которые он присылает обратно.
## Настройка

1) Необходимо создать группу Вконтакте. Перейти в управление, работа с API, создать ключ, в правах доступа разрешить управление сообществом, сообщения сообщества, фотографии, файлы.
2) Вставляем полученный API в код в переменную TOKEN вместо ```"YOUR_VK_TOKEN"```
3) Зайти в управление группой, перейти в сообщения и включить их
4) Далее, скачиваем ngrok. распаковываем архив в любую папку, копируем путь к папке и добавляем его в переменную PATH
5) Регистрируемся на сайте, пишем в консоль ```bash
   ngrok config add-authtoken $YOUR_AUTHTOKEN
   ```
   (ваш токен будет отображаться на сайте ngrok)
```bash
pip install -r requirements.txt
```
8) Вставляем в код вместо ```YOUR_CALLBACK_API_CODE``` значение, указанное в (Строка, которую должен вернуть сервер:), на странице Callback_API (управление, работа с API, callback API).
9) Запускаем код
10) Прописываем в bash консоль ```bash
ngrokk http 8000```

12) На странице Callback_API вставляем в поле Адрес то, что нам выдаёт консоль после исполнения 9) пункта после слова Forwarding (до символа ->).
13) Нажимаем подтвердить, должен прийти успешный ответ.
14) Готово! Вы можете писать в группу, а бот будет вам отвечать
