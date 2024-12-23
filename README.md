# README.md

## Weather Tracker Application

Это приложение для отслеживания погоды, разработанное с использованием Python и библиотеки Tkinter. Оно позволяет пользователям вводить URL-адреса для получения данных о погоде, сохранять эти данные и отображать их в графическом или табличном виде.

### Основные функции

- **Ввод URL**: Пользователь может ввести адрес страницы с данными о погоде.
- **Ввод Пути**: Пользователь может указать в диалоговом окне путь до директории, где будут сохраняться данные.
- **Сохранение данных**: Приложение сохраняет полученные с сайта данные о погоде в файле БД SQLite3
- **Частота обновления**: Пользователь может установить частоту считывания данных о погоде.
- **Графический интерфейс**: Удобный интерфейс для взаимодействия с приложением.
- **Информация о программе**: Возможность получения информации о приложении через меню.

### Установка

Для работы с приложением необходимо установить Python версии 3.x и библиотеки, используемые в проекте. Вы можете установить необходимые библиотеки с помощью pip:

```bash
pip install tkinter
```

### Запуск приложения

Чтобы запустить приложение, выполните следующий код:

```bash
python main.py
```

### Использование

1. **Ввод URL**:
   - Нажмите кнопку "GisMeteo" для открытия страницы сайта GisMeteo. Цвет кнопки изменится на красный
   - Скопируйте URL-адрес страницы с данными о погоде, перейдите в главное окно приложения и еще раз нажмите на эту же кнопку.
		Цвет кнопки вновь изменится и станет системным. Текст с адресом сайта появится в текстовом поле адреса сайта

2. **Сохранение пути**:
   - Нажмите кнопку "Путь" и укажите директорию для сохранения данных.

3. **Частота считывания данных**:
   - Нажмите кнопку "Как часто". Цвет кнопки изменится на красный. Текстовое поле станет активным. Введите число от 1 до 5,
		т.е. сколько раз в течении часа данные будут сохраняться в БД. Вновь нажмите на эту же кнопку с текстом "Сохранить".
		Цвет кнопки изменится на и станет системным. Текстовое окно станет недоступным для редактирования.

4. **Запуск приложения**:
   - Нажмите кнопку "Запустить" для начала отслеживания погоды. Цвет кнопки изменится на красный. Текст кнопки изменится на "Остановить"
		При повторном нажатии на эту же кнопку текст кнопки и ее цвет вновь изменятся на первоначальный. Процесс сбора и сохранения данных
		будет остановлен.
		Также, если приложение находится в режиме получения и сохранения данных, т.е. надпись на кнопке будет "Остановить" и цвет кнопки
		будет красный, кнопки изменения пути к директории, выбора адреса сайта и частоты обновлений данных будут заблокированы до тех пор,
		пока не будет остановлен процесс сбора данных.

5. **Выход из приложения**:
   - Нажмите кнопку "Выход" или закройте окно приложения.

### Структура проекта

- `main.py`: Главный файл приложения, содержащий логику и интерфейс.
- `info.json`: Файл для хранения настроек приложения и состояния.

### Лицензия

Этот проект лицензирован под MIT License. Вы можете использовать, изменять и распространять его в соответствии с условиями лицензии.

### Контакты

Если у вас есть вопросы или предложения по улучшению приложения, вы можете связаться с автором по электронной почте: [ваш_email@example.com].

---

Это README.md предоставляет полное представление о вашем проекте, включая его функции, инструкции по установке и запуску, а также информацию о структуре проекта и лицензии.
