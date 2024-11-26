import json
import os
from sys import float_info

import masterFiles

import tkinter as tk
import webbrowser
import datetime
import logging
from tkinter import Entry, Label, Button, StringVar, Toplevel, filedialog
from tkinter.messagebox import showinfo, askyesno

from masterFiles import FileOperation


class Window(tk.Tk):
    """Класс окна, наследуется от базового класс Tk модуля tkinter"""

    def __init__(self):
        """Конструктор класса"""
        super().__init__()
        self.filename_info = 'info.json'

        self.__width = 700  # ширина главного окна приложения
        self.__height = 270  # высота главного окна приложения
        #self.__direct = None    # директория для хранения файлов БД
        # self.__sity = None      # город, для которого формируют данные о погоде
        # self.__url = None       # сайт, из которого получают данные о погоде
        # self.__filename_bd = None   # сформированне полное имя файла БД
        # self.__time_repeat_task = None  # частота выполнения задачи
        # self.__is_job = None        # задача запущена или выполняется

        self.mf = FileOperation()   # атрибут храни объект класса для работы с файлами

        # переменные для привязки строковых данных к виджетам главного приложения
        #self.message_how_often = StringVar()
        self.__message_btn_url = StringVar()
        #self.message_path = StringVar()
        self.__message_btn_start = StringVar()

        self.__message_ent_path = StringVar()
        self.__message_ent_url = StringVar()
        self.__message_ent_how_ofthen = StringVar()

        self.lbl_url = Label(text='URL:')
        self.ent_url = Entry(width=92, text='',  textvariable=self.__message_ent_url)
        self.__message_btn_url.set('GisMeteo')
        self.btn_url_open = Button(width=9, text='Gismeteo', textvariable=self.__message_btn_url,
                                   command=self.click_btn_url_open)

        self.lbl_path = Label(text='Путь:')
        self.ent_path = Entry(width=92, text='',  textvariable=self.__message_ent_path)
        #self.message_path.set('Путь')
        self.btn_path_open = Button(width=9, text='Путь', command=self.click_btn_path_open)

        self.lbl_how_often = Label(text='Частота обновления данных с сайта GisMeteo. По умолчанию 1 раз в час:')
        self.ent_how_often = Entry(width=7, text='',  textvariable=self.__message_ent_how_ofthen)
        #self.message_how_ofthen.set('Как часто')
        self.btn_how_often_open = Button(width=9, text='Сохранить', command=self.click_btn_how_often_open)

        self.__message_btn_start.set('Запустить')
        self.btn_start = Button(width=12, text='Запустить', textvariable=self.__message_btn_start, command=self.click_btn_start)

        self.btn_show = Button(width=17, text='Показать данные')

        self.btn_exit = Button(width=12, text='Выход', command=self.window_destroy)

        self.ent_status_1 = Entry(width=50, text='', justify=tk.LEFT, state=tk.DISABLED)
        self.ent_status_2 = Entry(width=63, text='', justify=tk.RIGHT, state=tk.DISABLED)

        self.info = []  # создаем список
        self.info = list(self.mf.load_info(self.filename_info))
        self.__message_ent_url.set(self.info[0]['url'])
        self.__message_ent_path.set(self.info[0]['path'])
        self.__message_ent_how_ofthen.set(self.info[0]['how_often'])

        self.ent_url['state'] = tk.DISABLED
        self.ent_path['state'] = tk.DISABLED
        self.ent_how_often['state'] = tk.DISABLED

        self.title('Wheather - главный модуль')  # заголовок окна
        self.__set_plase_window_screen()  # метод устанавливает окно в указанной позиции дисплея
        self.__set_main_menu()  # метод создает меню

    def set_widget_plase(self):
        """Метод запрещает изменения размеров окна пользователем
        и позиционирует виджеты в окне"""
        self.resizable(False, False)

        self.lbl_path.place(x=13, y=12)
        self.ent_path.place(x=53, y=12)
        self.btn_path_open.place(x=620, y=7)

        self.lbl_url.place(x=13, y=41)
        self.ent_url.place(x=53, y=41)
        self.btn_url_open.place(x=620, y=36)

        self.lbl_how_often.place(x=13, y=70)
        self.ent_how_often.place(x=430, y=71)
        self.btn_how_often_open.place(x=620, y=65)

        self.btn_show.place(x=13, y=210)
        self.btn_start.place(x=495, y=210)
        self.btn_exit.place(x=597, y=210)

        self.ent_status_1.place(x=3, y=245)
        self.ent_status_2.place(x=310, y=245)


    def __set_plase_window_screen(self):
        """Метод получает данные о положении и размерах окна из словаря info
        и изменяет размеры и положение окна на дисплее"""
        geom = self.info[0]['wnd_geom']     # получаем значение geom именно из первого словаря списка
        self.geometry(geom)

    def window_destroy(self):
        """Функция информирует пользователя о попытке зsакрытия окна приложения и
         ждет подтверждения от пользователя. Если пользователь подтвердил свое решение
         о закрытии приложения, функция получает геометрические координаты окна на дисплее, сохраняет их в файл,
          удаляет и уничтожает все виджеты, расположенные в экземпляре окна
        и закрывает приложение"""

        # вызываем МеssageBox для подтвержения намерения закрытия окна приложения
        result = askyesno('Попытка закрыть окно', 'Вы действительно хотите закрыть приложение?')
        if not result: return
        # подтверждение получено. Получаем геометрические координаты окна и закрываем приложение
        wnd.update()  # обновить данные и получить строку с положением и размерами окна на дисплее
        geom = wnd.geometry()
        self.info[0]['wnd_geom'] = geom     # в сохраняем geom в первом словаре списка
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
        window.grab_release()       # освобождаем ресурсы пользовательского ввода
        window.destroy()            # уничтожаем дочернее окно

    @staticmethod
    def change_text_button(msg, old_text: str, new_text: str):
        """Метод меняет текст на кнопке,
        где: msg - переменная типа tkinter.StringVar, привязанная к конкретной кнопке,
        old_text - текст на кнопке, который был в момент клика по кнопке,
        new_old - текст, который будет установлен на кнопке"""
        text_btn = msg.get()
        if text_btn == old_text:
            msg.set(new_text)
        else:
            msg.set(old_text)
        return text_btn

    @staticmethod
    def change_color_button(obj, is_color: bool):
        """Метод изменяет цвет кнопки при клике на нее,
        где: obj - элемент класс Button,
        is_color - флаг, принимающий True, если меняем bg='red', fg='white'
        и False, если меняем цвет на bg='SystemButtonFace', fg='SystemButtonText'"""
        if is_color:
            obj.config(bg='red', fg='white')
        else:
            obj.config(bg='SystemButtonFace', fg='SystemButtonText')

    def click_btn_url_open(self):
        """Функция обработки клика по кнопке GisMeteo,
        где __message_btn_url - переменная типа tkinter.StringVar, объявленная ранее,
        old_text - текст на кнопке, который был в момент клика по кнопке,
        new_old - текст, который будет установлен на кнопке"""

        text_btn = self.change_text_button(self.__message_btn_url, 'GisMeteo', new_text='Сохранить')
        if text_btn == 'GisMeteo':
            # был клик по кнопке с надписью GisMeteo
            self.change_color_button(self.btn_url_open, True)   # изменим цвет кнопки на красный
            # выведем MessageBox с сообщением - инструкцией
            msg = (f'После открытия страницы сайта GisMeteo выполните следующие действия:\n'
                   f'1. В поле поиска введите название населенного пункта\n'
                   f'2. Перейдите на вкладку погоды "Сейчас" и скопируйте адрес страницы из браузера в буфер обмена.\n'
                   f'3. После того, как адрес страницы сайта будет скопирован и Вы вернетесь в программу,'
                   f'нажмите на кнопку "Сохранить". Она подсвечена красным цветом. Текст из буфера обмена будет вставлен в текстовое поле URL\n'
                   f'4. Подтвердите в новом информационном окне, что данные получены верно и их можно сохранять.')
            showinfo('Информация', msg)

            url = self.info[0]['url']
            logging.info(f'<{__name__}> Попытка запустить браузер и открыть страницу {url}')
            webbrowser.open_new(url) # откроем страницу в веббраузере

        else:
            # был клик по кнопке с надписью Сохранить
            self.change_color_button(self.btn_url_open, False)  # изменим цвет кнопки на системный
            str_url = wnd.clipboard_get()           # получим строку из буфера обмена
            str_url = str_url.strip()               # удалим возможные пробелы вначале и в конце строки

            # анализ строки https://www.gismeteo.ru/weather-leninsk-kuznetsky-11835/now/
            result = True   # считаем, что строка url верная
            if not 'https://www.gismeteo.ru/weather' in str_url:
                result = False
            if not '/now/' in str_url:
                result = False
            if not result:
                showinfo('Информация', 'Неверный адрес страницы сайти GisMeteo. Повторите выбор ...')
                logging.info(f'<{__name__}> Неверный выбор страницы сайта GisMeteo: {str_url}')
                return

            self.__message_ent_url.set(str_url)
            # Запрос на подтверждение выбора страницы сайта GisMeteo
            message = f'Подтвердите, что Вы ввели верный адрес страницы сайта'
            result = askyesno('Подтверждение', message)
            if not result:
                self.__message_ent_url.set('Адрес сайта указан неверно. Повторите выбор страницы сайта!')
                return

            # из полученной строки str_url выделим город
            index1 = str_url.find('-')
            index2 = str_url.rfind('-')
            sity = str_url[index1+1:index2]
            sity = sity.replace(' ', '_')
            sity = sity.replace('-', '_')

            # получим текущий год и сформируем имя файла БД
            dt = datetime.datetime.now()
            year = str(dt.year)
            name_bd = f'bd_{sity}_{year}.sqlite3'      # bd_leninsk_kuznetsky_2024.sqlite3

            path = self.info[0]['path']
            fullname_bd = f'{path}{name_bd}'

            self.info[0]['url'] = str_url  # сохраним полученный полученные данные в info
            self.info[0]['sity'] = sity
            #self.info[0]['how_often'] = 1
            self.info[0]['name_bd'] = name_bd
            self.info[0]['fullname_bd'] = fullname_bd
            #self.info[0]['is_job'] = 0

            self.mf.save_info(self.filename_info, self.info)



    def click_btn_path_open(self):
        """Функция обработки клика по кнопке Путь
            где message_path - переменная типа tkinter.StringVar, объявленная ранее,
            old_text - текст на кнопке, который был в момент клика по кнопке,
            new_old - текст, который будет установлен на кнопке"""

        direct = filedialog.askdirectory(title='Выбор директории для хранения файлов базы данных', initialdir="C:\\")
        if not os.path.exists(direct):
            message = f'Выбранной Вами директории не существует. Повторите выбор директории'
            showinfo('Информация', message)
            return
        else:

            #self.insert_str_in_entry(self.ent_path, direct)
            self.ent_path['state'] = tk.NORMAL
            self.__message_ent_path.set(direct)
            self.ent_path['state'] = tk.DISABLED
            message = f'Вы действительно хотите выбрать эту директорию для хранения фалов базы данных?'
            result = askyesno('Информация', message)
            if not result:
                self.ent_path['state'] = tk.NORMAL
                self.__message_ent_path.set(self.info[0]['path'])
                self.ent_path['state'] = tk.DISABLED
                return
            direct = direct.replace('/', '\\')
            self.info[0]['path'] = direct + '\\'
            self.mf.save_info(self.filename_info, self.info)



    def click_btn_how_often_open(self):
        """Функция обработки клика по кнопке Как часто
            где message_how_ofthen - переменная типа tkinter.StringVar, объявленная ранее,
            old_text - текст на кнопке, который был в момент клика по кнопке,
            new_old - текст, который будет установлен на кнопке"""
        pass

        # text_btn = self.change_text_button(self.message_how_ofthen, 'Как часто', 'Сохранить')
        # if text_btn == 'Как часто':
        #     # был клик по кнопке с надписью Как часто
        #     self.change_color_button(self.btn_how_often_open, True)
        #     print(text_btn)
        #
        # else:
        #     # был клик по кнопке с надписью Сохранить
        #     self.change_color_button(self.btn_how_often_open, False)
        #     print(text_btn)

    def click_btn_start(self):
        """Функция обработки клика по кнопке
            где message_path - переменная типа tkinter.StringVar, объявленная ранее,
            old_text - текст на кнопке, который был в момент клика по кнопке,
            new_old - текст, который будет установлен на кнопке"""

        text_btn = self.change_text_button(self.__message_btn_start, 'Запустить', 'Остановить')
        if text_btn == 'Запустить':
            # был клик по кнопке с надписью Путь
            self.change_color_button(self.btn_start, True)
            print(text_btn)
        else:
            # был клик по кнопке с надписью Сохранить
            self.change_color_button(self.btn_start, False)
            print(text_btn)

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
    wnd.set_widget_plase()


    wnd.protocol("WM_DELETE_WINDOW", wnd.window_destroy)

    wnd.mainloop()
