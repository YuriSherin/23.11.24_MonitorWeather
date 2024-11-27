import tkinter as tk
import webbrowser
import datetime
import logging
from tkinter import Entry, Label, Button, StringVar, Toplevel, filedialog, ttk
from tkinter.messagebox import showinfo, askyesno

from masterFiles import FileOperation


class Window(tk.Tk):
    """Класс окна, наследуется от базового класс Tk модуля tkinter"""

    def __init__(self):
        """Конструктор класса"""
        super().__init__()
        self.__width = 590  # ширина главного окна приложения
        self.__height = 230  # высота главного окна приложения
        self.filename_info = 'info.json'
        self.mf = FileOperation()   # атрибут храни объект класса для работы с файлами

        self.info = {}  # создаем словарь, в котором будет содержать информация из файла 'info.json'
        if self.mf.is_exist_file(self.filename_info):   # если файл существует
            self.info = self.mf.load_info(self.filename_info)   # прочитаем данные из файла
        else:
            self.create_new_file_json()     # создадим словарь с данными по умолчанию и сохраним его

        # переменные для привязки строковых данных к виджетам главного приложения
        #self.__message_btn_often = StringVar()  # привязка строковых данных к тексту кнопки Как часто / Сохранить
        self.__message_btn_url = StringVar()    # привязка строковых данных к тексту кнопки GisMeteo / Сохранить
        self.__message_btn_start = StringVar()  # привязка строковых данных к тексту кнопки Запустить / Остановить

        self.__message_ent_path = StringVar()   # привязка строковых данных к текстовому полю Путь
        self.__message_ent_url = StringVar()    # привязка строковых данных к текстовому полю URL
        #self.__message_ent_often = StringVar()     # привязка строковых данных к текстовому полю Как часто

        combo_lst = ['0 час. 10 мин.', '0 час. 20 мин.', '0 час. 30 мин.', '1 час. 00 мин.', '1 час. 30 мин.',
                     '2 час. 00 мин.', '4 час. 00 мин']
        self.__message_combo = StringVar(value=combo_lst[3])

        """Создадим виджеты главного окна приложения"""
        # строка виджетов URL
        self.lbl_url = tk.Label(text='URL: ', fg='darkblue')  # надпись
        self.lbl_url.grid(row=0, column=0, padx=5, pady=2, sticky='w')
        self.txt_url = tk.Entry(text='', width=70, textvariable=self.__message_ent_url)  # текстовое поле
        self.txt_url.grid(row=0, column=1, columnspan=3, padx=5, pady=2)
        self.__message_btn_url.set('GisMeteo')
        self.btn_url = tk.Button(text='GisMeteo', width=12, textvariable=self.__message_btn_url, command=self.click_btn_url_open)  # кнопка
        self.btn_url.grid(row=0, column=4, padx=5, pady=2)


        # строка виджетов Путь
        self.lbl_path = tk.Label(text='Путь: ', fg='darkblue')  # надпись
        self.lbl_path.grid(row=1, column=0, padx=5, pady=2, sticky='w')
        self.txt_path = tk.Entry(text='', width=70, textvariable=self.__message_ent_path)  # текстовое поле
        self.txt_path.grid(row=1, column=1, columnspan=3, padx=5, pady=2)
        #self.__message_btn_often.set('Как часто')
        self.btn_path = tk.Button(text='Путь', width=12, command=self.click_btn_path)  # кнопка
        self.btn_path.grid(row=1, column=4, padx=5, pady=2)


        # строка виджетов Как часто
        self.lbl_often = tk.Label(text='Обновление данных через:', fg='darkblue')  # надпись
        self.lbl_often.grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky='w')

        self.combo_often = ttk.Combobox(width=14, values=combo_lst, textvariable=self.__message_combo, justify="center",  state='readonly')
        self.combo_often.grid(row=2, column=2, padx=5, pady=2, sticky='w')
        self.combo_often.bind("<<ComboboxSelected>>", self.select_combo_box)
        # установка времени в combo_often из словаря info
        select_time = self.info['select_time']
        index = -1
        for item in combo_lst:
            index += 1
            if item == select_time:
                break
        self.combo_often.current(index)

        # 3 строки - резерв
        self.lbl_empty_1 = tk.Label(text='', height=1).grid(row=3, column=0)
        self.lbl_empty_2 = tk.Label(text='', height=1).grid(row=4, column=0)
        self.lbl_empty_3 = tk.Label(text='', height=1).grid(row=5, column=0)

        # строка кнопок управления
        self.btn_exit = tk.Button(text='Выход', width=12, command=self.window_destroy)  # кнопка
        self.btn_exit.grid(row=6, column=4, pady=10)
        self.__message_btn_start.set('Запустить')
        self.btn_start = tk.Button(text='Запустить', width=12, textvariable=self.__message_btn_start, command=self.click_btn_start)  # кнопка
        self.btn_start.grid(row=6, column=3, sticky='e')
        self.btn_show = tk.Button(text='Показать данные', width=15)  # кнопка
        self.btn_show.grid(row=6, column=1, columnspan=2, sticky='w')

        """Настройка отображения текстовых полей и кнопок"""
        self.__message_ent_url.set(self.info['url'])
        self.__message_ent_path.set(self.info['path'])
        #self.__message_ent_often.set(self.info['how_often'])
        self.txt_url['state'] = tk.DISABLED  # текстовое поле недоступно для редактирования
        self.txt_path['state'] = tk.DISABLED  # текстовое поле недоступно для редактирования
        #self.txt_often['state'] = tk.DISABLED  # текстовое поле недоступно для редактирования
        self.combo_often['state'] = tk.DISABLED

        if self.info['is_job']:
            # процесс сбора данных запущен в фоновом
            self.change_text_button(self.__message_btn_start, 'Запустить', 'Остановить')
            self.change_color_button(self.btn_start, True)
            # блокируем кнопки. Во время получения информации нельзя редактировать откуда получать и куда сохранять
            self.btn_url['state'] = tk.DISABLED
            self.btn_path['state'] = tk.DISABLED
            self.combo_often['state'] = tk.DISABLED

        else:
        # процесс сбора данных остановлен
            # разблокируем кнопки. Сбор информации остановлен
            self.btn_url['state'] = tk.NORMAL
            self.btn_path['state'] = tk.NORMAL
            self.combo_often['state'] = tk.NORMAL



        # строка поля статус
        self.txt_status1 = tk.Entry(text='', width=5)  # текстовое поле
        self.txt_status1.grid(row=7, column=0, columnspan=2, padx=2, pady=2, sticky='we')
        self.txt_status1['state'] = tk.DISABLED

        self.txt_status2 = tk.Entry(text='', width=5)  # текстовое поле
        self.txt_status2.grid(row=7, column=2, columnspan=3, padx=2, pady=2, sticky='we')
        self.txt_status2['state'] = tk.DISABLED

        self.__set_plase_window_screen()    # установка размеров и положения окна на дисплее
        self.__set_main_menu()              # подключение меню главного окна приложения

# ================== Исправленные методы ==============================
    def __set_plase_window_screen(self):
        """Метод получает данные о положении и размерах окна из словаря info
        и изменяет размеры и положение окна на дисплее"""
        geom = self.info['wnd_geom']     # получаем значение geom именно из первого словаря списка
        self.geometry(geom)

    def create_new_file_json(self):
        """Метод вызывается, когда отсутствует файл 'info.json'.
        Он заполняет атрибут объекта info дефолтными данными
        и сохраняет их в файл"""
        self.info.clear()       # очистим словарь info
        # добавим в атрибут объекта словарь дефолтные данные
        self.info = {
            "wnd_geom": "586x222+618+389",
            "url": "https://www.gismeteo.ru/weather-leninsk-kuznetsky-11835/now/",
            "path": "D:\\SQLite\\Weather\\",
            "sity": "leninsk_kuznetsky",
            "select_time": "1 час. 30 мин.",
            "name_bd": "bd_leninsk_kuznetsky_2024.sqlite3",
            "fullname_bd": "C:\\Users\\yuris\\Downloads\\Telegram Desktop\\bd_leninsk_kuznetsky_2024.sqlite3",
            "is_job": 0,
            "how_often": 1
            }
        self.mf.save_info(self.filename_info, self.info)    # сохраним словарь в файл

    def window_destroy(self):
        """Метод информирует пользователя о попытке закрытия окна приложения и
         ждет подтверждения от пользователя. Если пользователь подтвердил свое решение
         о закрытии приложения, функция получает геометрические координаты окна на дисплее, сохраняет их в файл,
          удаляет и уничтожает все виджеты, расположенные в экземпляре окна
        и закрывает приложение"""
        logging.info(f'<{__name__}> КЛИЕ по кнопке "Выход"')
        # вызываем МеssageBox для подтвержения намерения закрытия окна приложения
        result = askyesno('Попытка закрыть окно', 'Вы действительно хотите закрыть приложение?')
        if not result:
            logging.info(f'<{__name__}> НЕ ПОЛУЧЕНО подтверждение на выход из приложения"')
            return
        # подтверждение получено. Получаем геометрические координаты окна и закрываем приложение
        logging.info(f'<{__name__}>ПОЛУЧЕНО подтверждение на выход из приложения"')
        wnd.update()  # обновить данные и получить строку с положением и размерами окна на дисплее
        geom = wnd.geometry()
        self.info['wnd_geom'] = geom     # в сохраняем geom в первом словаре списка
        self.mf.save_info(self.filename_info, self.info)

        wnd.destroy()  # уничтожаем все виджеты, расположенные на окне
        exit(0)  # выходим из программы с кодом 0

    def __set_main_menu(self):
        """Метод создает меню приложения"""
        main_menu = tk.Menu()  # создаем объект меню
        self.config(menu=main_menu)  #
        file_menu = tk.Menu(tearoff=0)  # подменю не сможет быть отсоединено

        # создаем подменю пункта меню Файл
        file_menu.add_separator()
        file_menu.add_command(label='Выход', command=self.window_destroy)

        # создаем подменю пункта меню О программе
        about_nemu = tk.Menu(tearoff=0)
        about_nemu.add_command(label='О программе', command=self.__about_wnd_child)

        # Устанавливаем пункты меню вместе с пунктами подменю
        main_menu.add_cascade(label='Файл', menu=file_menu)
        main_menu.add_cascade(label='Помощь', menu=about_nemu)

    def __about_wnd_child(self):
        """Метод создает дочернее окно О программе указанных размеров
        в центре дисплея. В это дочернее окно помещается виджет Text,
        а уже в нем выводится информация"""
        wnd_child_about = Toplevel(bg='lightyellow')
        wnd_child_about.title("О программе")
        w, h = 350, 150  # ширина и высота окна
        # расчет позиции окна для вывода в центр дисплея
        sw = self.winfo_screenwidth()  # получим ширину экрана монитора
        sh = self.winfo_screenheight()  # получим высоту экрана монитора
        x = (sw - w) // 2
        y = (sh - h) // 2
        geom = f'{w}x{h}+{x}+{y}'
        wnd_child_about.geometry(geom)
        # создаем виджет Text и вствляем в него строку текста
        text_edit_child = tk.Text(wnd_child_about, bg='darkblue', fg='white', wrap='word')
        msg = (f'Эта программа отслеживает погоду в указанном Вами населенном пункте, '
               f'сохраняет полученные данные в базу данных SQLite3 и по Вашей команде выводит эти данные '
               f'в графическом или табличном виде\n\n'
               f'Версия: 1.0\n2024 г.')
        text_edit_child.insert("1.0", msg)
        text_edit_child.pack(fill='both', expand=1)
        wnd_child_about.resizable(False, False)
        wnd_child_about.protocol("WM_DELETE_WINDOW", lambda: self.__wnd_child_about_exit(
            wnd_child_about))  # перехватываем нажатие на крестик
        wnd_child_about.grab_set()  # захватываем пользовательский ввод

    @staticmethod
    def __wnd_child_about_exit(window):
        """Метод освобождает ресурсы и удаляет дочернее окно"""
        window.grab_release()  # освобождаем ресурсы пользовательского ввода
        window.destroy()  # уничтожаем дочернее окно

    @staticmethod
    def change_text_button(var, old_text: str, new_text: str):
        """Метод меняет текст на кнопке,
        где: msg - переменная типа tkinter.StringVar, привязанная к конкретной кнопке,
        old_text - текст на кнопке, который был в момент клика по кнопке,
        new_old - текст, который будет установлен на кнопке"""
        text_btn = var.get()
        if text_btn == old_text:
            var.set(new_text)
        else:
            var.set(old_text)
        return text_btn

    @staticmethod
    def change_color_button(obj, is_color: bool):
        """Метод изменяет цвет кнопки при клике на нее,
        где: obj - элемент класс Button,
        is_color - флаг, принимающий True, если меняем bg='red', fg='white'
        и False, если меняем цвет на bg='SystemButtonFace', fg='SystemButtonText'"""
        if is_color:
            obj.config(bg='red', fg='white')
            logging.info(f'<{__name__}> Цвет кнопки изменен на bg="red", fg="white"')
        else:
            obj.config(bg='SystemButtonFace', fg='SystemButtonText')
            logging.info(f'<{__name__}> Цвет кнопки изменен на bg="SystemButtonFace", fg="SystemButtonText"')


    def click_btn_start(self):
        """Метод обработки клика по кнопке Запустить / Остановить"""

        logging.info(f'<{__name__}> Клик по кнопке {self.__message_btn_start.get()}')

        # изменим старый текст кнопки на новый, хотя в text_btn вернется старый текст
        text_btn = self.change_text_button(self.__message_btn_start, 'Запустить', 'Остановить')

        logging.info(f'<{__name__}> Текст кнопки изменен на  {self.__message_btn_start.get()}')
        if text_btn == 'Запустить':
            # был клик по кнопке с надписью Запустить
            self.change_color_button(self.btn_start, True)
            self.info['is_job'] = 1
            logging.info(f'<{__name__}> Процесс сбора данных ЗАПУЩЕН')
            #блокируем кнопки
            self.btn_url['state'] = tk.DISABLED
            self.btn_path['state'] = tk.DISABLED

            self.combo_often['state'] = tk.DISABLED
        else:
            # был клик по кнопке с надписью Остановить
            self.change_color_button(self.btn_start, False)
            self.info['is_job'] = 0
            logging.info(f'<{__name__}> Процесс сбора данных ОСТАНОВЛЕН')
            # разблокируем кнопки
            self.btn_url['state'] = tk.NORMAL
            self.btn_path['state'] = tk.NORMAL
            self.combo_often['state'] = tk.NORMAL

        self.mf.save_info(self.filename_info, self.info)        # сохраняем данные в файл


    def click_btn_url_open(self):
        """Метод обработки клика по кнопке GisMeteo"""

        logging.info(f'<{__name__}> Клик по кнопке {self.__message_btn_url.get()}')
        # изменим старый текст кнопки на новый, хотя в text_btn вернется старый текст
        text_btn = self.change_text_button(self.__message_btn_url, 'GisMeteo', new_text='Сохранить')
        logging.info(f'<{__name__}> Текст кнопки изменен на  {self.__message_btn_url.get()}')

        if text_btn == 'GisMeteo':
            # был клик по кнопке с надписью GisMeteo
            self.change_color_button(self.btn_url, True)   # изменим цвет кнопки на красный
            # выведем MessageBox с сообщением - инструкцией
            msg = (f'После открытия страницы сайта GisMeteo выполните следующие действия:\n'
                   f'1. В поле поиска введите название населенного пункта\n'
                   f'2. Перейдите на вкладку погоды "Сейчас" и скопируйте адрес страницы из браузера в буфер обмена.\n'
                   f'3. После того, как адрес страницы сайта будет скопирован и Вы вернетесь в программу,'
                   f'нажмите на кнопку "Сохранить". Она подсвечена красным цветом. Текст из буфера обмена будет вставлен в текстовое поле URL\n'
                   f'4. Подтвердите в новом информационном окне, что данные получены верно и их можно сохранять.')
            showinfo('Информация', msg)

            url = self.info['url']
            logging.info(f'<{__name__}> Попытка запустить браузер и открыть страницу {url}')
            webbrowser.open_new(url) # откроем страницу в веббраузере

        else:
            # был клик по кнопке с надписью Сохранить
            #logging.info(f'<{__name__}> Клик по кнопке {self.__message_btn_url.get()}')
            self.change_color_button(self.btn_url, False)  # изменим цвет кнопки на системный
            str_url = wnd.clipboard_get()           # получим строку из буфера обмена
            str_url = str_url.strip()               # удалим возможные пробелы вначале и в конце строки

            # анализ строки https://www.gismeteo.ru/weather-leninsk-kuznetsky-11835/now/
            logging.info(f'<{__name__}>Проверка полученной строки {str_url}')
            result = True   # считаем, что строка url верная
            if not 'https://www.gismeteo.ru/weather' in str_url:
                result = False
            if not '/now/' in str_url:
                result = False
            if not result:
                showinfo('Информация', 'Неверный адрес страницы сайти GisMeteo. Повторите выбор ...')
                logging.info(f'<{__name__}> Полученный URL не является адресом страницы сайта GisMeteo: {str_url}')
                return
            logging.info(f'<{__name__}>Адрес страницы сайте GisMeteo соответствует полученной строке: {str_url}')
            self.txt_url['state'] = tk.NORMAL
            self.__message_ent_url.set(str_url)
            self.txt_url['state'] = tk.DISABLED
            # Запрос на подтверждение выбора страницы сайта GisMeteo
            message = f'Подтвердите, что Вы ввели верный адрес страницы сайта'
            result = askyesno('Подтверждение', message)
            if not result:
                self.txt_url['state'] = tk.NORMAL
                self.__message_ent_url.set('Адрес сайта указан неверно. Повторите выбор страницы сайта!')
                self.txt_url['state'] = tk.DISABLED
                logging.info(f'<{__name__}>Не получено подтверждения верного URL: {str_url}')
                return

            # из полученной строки str_url выделим город
            logging.info(f'<{__name__}>Анализ полученной строки {str_url}')
            # получим из строки URL населенный пункт
            index1 = str_url.find('-')
            index2 = str_url.rfind('-')
            sity = str_url[index1+1:index2]
            # удалим все возможные пробелы и заменим '-' на '_'
            sity = sity.replace(' ', '_')
            sity = sity.replace('-', '_')

            # получим текущий год и сформируем имя файла БД
            dt = datetime.datetime.now()
            year = str(dt.year)
            name_bd = f'bd_{sity}_{year}.sqlite3'      # bd_leninsk_kuznetsky_2024.sqlite3

            path = self.info['path']    # путь берем из info, потому что возможно его не нужно обновлять
            # проверим, что такой путь существует
            if not self.mf.is_exist_file(path):
                # неверно указан путь до хранения файлов БД
                message = f'Неверный путь до директории с файлами БД {path}. Укажите верный путь.'
                showinfo('Информация', message)
                return

            fullname_bd = f'{path}{name_bd}'

            self.info['url'] = str_url  # сохраним полученный полученные данные в info
            self.info['sity'] = sity
            self.info['how_often'] = 1
            self.info['name_bd'] = name_bd
            self.info['fullname_bd'] = fullname_bd
            self.info['is_job'] = 0

            self.mf.save_info(self.filename_info, self.info)    # сохраним данные в файл



    def click_btn_path(self):
        """Метод обработки клика по кнопке Путь"""

        logging.info(f'<{__name__}> Клик по кнопке "Путь"')
        direct = filedialog.askdirectory(title='Выбор директории для хранения файлов базы данных', initialdir="C:\\")
        if not self.mf.is_exist_file(direct):
            message = f'Выбранной Вами директории "{direct}" не существует. Повторите выбор директории'
            showinfo('Информация', message)
            return
        else:

            #self.insert_str_in_entry(self.ent_path, direct)
            self.txt_path['state'] = tk.NORMAL
            self.__message_ent_path.set(direct)
            self.txt_path['state'] = tk.DISABLED
            message = f'Вы действительно хотите выбрать эту директорию для хранения фалов базы данных?'
            result = askyesno('Информация', message)

            if not result:      # если подтверждения нет, восстановим путь из словаря info
                self.txt_path['state'] = tk.NORMAL
                self.__message_ent_path.set(self.info['path'])
                self.txt_path['state'] = tk.DISABLED
                logging.info(f'<{__name__}>НЕ ПОДТВЕРЖДЕН выбраный путь {direct}')
                return

            logging.info(f'<{__name__}>ПОДТВЕРЖДЕН выбраный путь {direct}')
            direct = direct.replace('/', '\\')
            self.info['path'] = direct + '\\'                   # изменим путь в словаре info
            self.mf.save_info(self.filename_info, self.info)    # сохраним путь в файл


    def select_combo_box(self, event):
        """Метод изменения выбора времени обновления данных"""
        logging.info(f'<{__name__}>ИЗМЕНЕНИЕ выбора времени получения данных')
        selection = self.combo_often.get()     # получили выбранное время
        logging.info(f'<{__name__}>НОВОЕ ВРЕМЯ получения данных {selection}')
        self.info['select_time'] = selection
        self.mf.save_info(self.filename_info, self.info)

    # =====================================================================

    def insert_str_in_entry(self, obj, msg: str):
        """Функция помещает текстовое сообщение в статусную строку.
        где: obj - экземпляр класса Entry,
        msg - сообщение, которое необходимо поместить"""
        # запись текста в статусную строку
        obj['state'] = tk.NORMAL
        obj.insert(0, msg)
        obj['state'] = tk.DISABLED



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", encoding='utf8')#,
    wnd = Window()  # создаем объект главного окна с указанными размерами



    wnd.protocol("WM_DELETE_WINDOW", wnd.window_destroy)
    wnd.mainloop()


