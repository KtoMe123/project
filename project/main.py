import wx
from selenium import webdriver
from selenium.common.exceptions import *
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

APP_EXIT = 1
class MyFrame(wx.Frame):
    webdriver_path = GeckoDriverManager().install()

    service = Service(webdriver_path)
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    browser = webdriver.Firefox(service=service, options=options)

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300,200))


        menubar = wx.MenuBar()
        fileMenu = wx.Menu()

        item = fileMenu.Append(APP_EXIT, "Выход", "Выход из приложения")


        menubar.Append(fileMenu, "&Menu")
        self.SetMenuBar(menubar)


        self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)




        #Наполнение страницы
        self.panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # -----------------------

        btnItem = wx.Button(self.panel, label="        НАЙТИ ПРЕДМЕТ        ")
        sizer.Add(btnItem, flag=wx.CENTRE | wx.UP, border=15)

        btnItem.Bind(wx.EVT_BUTTON, self.Item)


        # -----------------------
        btnAir = wx.Button(self.panel, label="НАЙТИ БИЛЕТ САМОЛЕТА")
        sizer.Add(btnAir, flag=wx.CENTRE | wx.UP, border=15)

        btnAir.Bind(wx.EVT_BUTTON, self.Air)

        # -----------------------
        btnHost = wx.Button(self.panel, label="       НАЙТИ ЖД БИЛЕТ        ")
        sizer.Add(btnHost, flag=wx.CENTRE | wx.UP, border=15)

        btnHost.Bind(wx.EVT_BUTTON, self.JD)


        self.panel.SetSizer(sizer)



    def onQuit(self, event):
        self.Close()

    def Item(self, event):
        print('nice1')
        dlg = SerchItem()
        dlg.ShowModal()

    def Air(self, event):
        print('nice2')
        dlg = SerchAir()
        dlg.ShowModal()

    def JD(self, event):
        print('nice3')
        dlg = SerchJD()
        dlg.ShowModal()



class SerchItem(wx.Dialog):
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Search Item", size=(300,150))



        item_sizer = wx.BoxSizer(wx.HORIZONTAL)

        Item = wx.StaticText(self, label="Название предмета:")
        item_sizer.Add(Item, 0, wx.ALL | wx.CENTER, 5)
        self.Item = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.Item.Bind(wx.EVT_TEXT_ENTER, self.SearchItem)
        item_sizer.Add(self.Item, 0, wx.ALL, 5)





        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(item_sizer, 0, wx.ALL, 5)

        main_sizer.Add(wx.StaticLine(self), flag=wx.EXPAND | wx.CENTRE | wx.UP, border=30)

        btn = wx.Button(self, label="Показать")
        btn.Bind(wx.EVT_BUTTON, self.SearchItem)
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 7)



        self.SetSizer(main_sizer)



    def SearchItem(self, event):

        Item = self.Item.GetValue()

        browser = MyFrame.browser


        browser.get('https://www.ebay.com/')

        time.sleep(1)
        search_bar = browser.find_element(By.ID, 'gh-ac')
        search_bar.send_keys(Item)

        time.sleep(3)
        button = browser.find_element(By.ID, 'gh-btn')
        button.click()

        time.sleep(2)
        product_check = browser.find_element(By.XPATH, '/html/body/div[8]/div[4]/div[1]/div/div[2]/div[1]/div[1]/h1/span[1]')
        product_check1 = product_check.text

        if product_check1 == '0':
            error_dlg = wx.MessageDialog(self, "Товар не найден! ", "ERROR", wx.OK_DEFAULT | wx.ICON_ERROR)

            if error_dlg == wx.ID_OK:
                print('OK')
            error_dlg.ShowModal()
        time.sleep(1)

        product_price = browser.find_element(By.XPATH, '/html/body/div[8]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[2]/div[3]/div[1]/span')

        product_name = browser.find_element(By.XPATH, '/html/body/div[8]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[2]/a/div/span')


        price = product_price.text
        name = product_name.text
        main_dlg = wx.MessageDialog(self, f"Цена: {price}\nНазвание: {name} ", "Info", wx.OK_DEFAULT)

        if main_dlg == wx.ID_OK:
            print('OK')
        main_dlg.ShowModal()

        print(product_check1)
        print(price)
        print(name)


        print(Item)

class SerchAir(wx.Dialog):
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Search avia", size=(300,250))



        posadka_sizer = wx.BoxSizer(wx.HORIZONTAL)

        posadka = wx.StaticText(self, label="Город посадки:                   ")
        posadka_sizer.Add(posadka, 0, wx.ALL | wx.CENTER, 5)
        self.posadka = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        posadka_sizer.Add(self.posadka, 0, wx.ALL, 5)

        vibsodka_sizer = wx.BoxSizer(wx.HORIZONTAL)

        vibsodka = wx.StaticText(self, label="Город высадки:                  ")
        vibsodka_sizer.Add(vibsodka, 0, wx.ALL | wx.CENTER, 5)
        self.vibsodka = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        vibsodka_sizer.Add(self.vibsodka, 0, wx.ALL, 5)

        data_sizer = wx.BoxSizer(wx.HORIZONTAL)

        data = wx.StaticText(self, label="Дата посадки (xx.xx.xxxx):")
        data_sizer.Add(data, 0, wx.ALL | wx.CENTER, 5)
        self.data = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.data.Bind(wx.EVT_TEXT_ENTER, self.SearchAir)
        data_sizer.Add(self.data, 0, wx.ALL, 5)


        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(posadka_sizer, 0, wx.ALL, 5)
        main_sizer.Add(vibsodka_sizer, 0, wx.ALL, 5)
        main_sizer.Add(data_sizer, 0, wx.ALL, 5)

        main_sizer.Add(wx.StaticLine(self), flag=wx.EXPAND | wx.CENTRE | wx.UP, border=30)

        btn = wx.Button(self, label="Показать")
        btn.Bind(wx.EVT_BUTTON, self.SearchAir)
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 7)



        self.SetSizer(main_sizer)



    #сохраняем данные
    def SearchAir(self, event):

        Posadka = self.posadka.GetValue()
        Visodka = self.vibsodka.GetValue()
        Data = self.data.GetValue()

        browser = MyFrame.browser

        browser.get('https://avia.tutu.ru/')
        time.sleep(1)

        otkuda = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div/div[1]/span/div/div/input')
        otkuda.send_keys('q')
        otkuda.clear()
        kuda = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/span/div/div/input')
        kuda.send_keys('q')
        kuda.clear()
        kogda = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/div/input')
        kogda.send_keys('q')
        kogda.clear()
        time.sleep(1)

        otkuda.send_keys(Posadka)
        time.sleep(1.5)
        kuda.send_keys(Visodka)
        time.sleep(1.5)
        kogda.send_keys(Data)

        button = browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/button')
        button.click()

        time.sleep(1.5)
       # skolko = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[2]/div[1]')
       # skolko_error = skolko.text
        skolko2 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[1]')
        skolko_error2 = skolko2.text
        skolko3 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[2]')
        skolko_error3 = skolko3.text

      # if skolko_error == 'Нет билетов на эту дату':
        #    error_dlg = wx.MessageDialog(self, "Мы не нашли билет на выбранную дату! ", "ERROR", wx.OK_DEFAULT | wx.ICON_ERROR)

      #      if error_dlg == wx.ID_OK:
       #         print('OK')
       #     error_dlg.ShowModal()

        if skolko_error2 == 'Мы не нашли билеты на самолëт на выбранную дату':
            error_dlg = wx.MessageDialog(self, "Мы не нашли билет на выбранную дату! ", "ERROR", wx.OK_DEFAULT | wx.ICON_ERROR)

            if error_dlg == wx.ID_OK:
                print('OK')
            error_dlg.ShowModal()

        if skolko_error3 == 'Мы не нашли билеты на самолëт на выбранную дату':
            error_dlg = wx.MessageDialog(self, "Мы не нашли билет на выбранную дату! ", "ERROR", wx.OK_DEFAULT | wx.ICON_ERROR)

            if error_dlg == wx.ID_OK:
                print('OK')
            error_dlg.ShowModal()

        vrem9_vzleta_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div/div[1]/span[1]')
        vrem9_vzleta = vrem9_vzleta_path.text

        data_vzleta_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div/div[1]/span[2]')
        data_vzleta = data_vzleta_path.text

        vrem9_posadki_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/span[1]')
        vrem9_posadki = vrem9_posadki_path.text

        # data_posadki_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div[1]/span[2]')
        # data_posadki = data_posadki_path.text

        price_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[2]/div/div/div[1]/div/button[1]/div[2]/div/div/span')
        price = price_path.text

        peresadki_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[3]/div[1]/span/span/span/span')
        peresadki = peresadki_path.text

        vzlet_obh_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div')
        vzlet_obh = vzlet_obh_path.text

        posadka_obh_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div')
        posadka_obh = posadka_obh_path.text

        main_dlg = wx.MessageDialog(self, f"Взлет: {vzlet_obh}\nПосадка: {posadka_obh}\nЦена: {price}\nРейс:{peresadki} ", "Info", wx.OK_DEFAULT)

        if main_dlg == wx.ID_OK:
            print('OK')
        main_dlg.ShowModal()


        print(vrem9_vzleta)
        print(data_vzleta)
        print(vrem9_posadki)
        print(price)
        print(peresadki)
        print(vzlet_obh)
        print(posadka_obh)


class SerchJD(wx.Dialog):
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Search JD", size=(300,250))



        posadka_sizer = wx.BoxSizer(wx.HORIZONTAL)

        posadka = wx.StaticText(self, label="Город посадки:                   ")
        posadka_sizer.Add(posadka, 0, wx.ALL | wx.CENTER, 5)
        self.posadka = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        posadka_sizer.Add(self.posadka, 0, wx.ALL, 5)

        vibsodka_sizer = wx.BoxSizer(wx.HORIZONTAL)

        vibsodka = wx.StaticText(self, label="Город высадки:                  ")
        vibsodka_sizer.Add(vibsodka, 0, wx.ALL | wx.CENTER, 5)
        self.vibsodka = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        vibsodka_sizer.Add(self.vibsodka, 0, wx.ALL, 5)

        data_sizer = wx.BoxSizer(wx.HORIZONTAL)

        data = wx.StaticText(self, label="Дата посадки (xx.xx.xxxx):")
        data_sizer.Add(data, 0, wx.ALL | wx.CENTER, 5)
        self.data = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.data.Bind(wx.EVT_TEXT_ENTER, self.SearchJD)
        data_sizer.Add(self.data, 0, wx.ALL, 5)


        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(posadka_sizer, 0, wx.ALL, 5)
        main_sizer.Add(vibsodka_sizer, 0, wx.ALL, 5)
        main_sizer.Add(data_sizer, 0, wx.ALL, 5)

        main_sizer.Add(wx.StaticLine(self), flag=wx.EXPAND | wx.CENTRE | wx.UP, border=30)

        btn = wx.Button(self, label="Показать")
        btn.Bind(wx.EVT_BUTTON, self.SearchJD)
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 7)



        self.SetSizer(main_sizer)



    #сохраняем данные
    def SearchJD(self, event):

        Posadka = self.posadka.GetValue()
        Visodka = self.vibsodka.GetValue()
        Data = self.data.GetValue()

        browser = MyFrame.browser

        browser.get('https://www.tutu.ru/poezda/')
        time.sleep(1)
        otkuda = browser.find_element(By.NAME, 'schedule_station_from')
        otkuda.send_keys('q')
        otkuda.clear()
        kuda = browser.find_element(By.NAME, 'schedule_station_to')
        kuda.send_keys('q')
        kuda.clear()
        kogda = browser.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/form/div/div/div[4]/div/div[1]/div/input')
        kogda.send_keys('q')
        kogda.clear()

        time.sleep(1)

        otkuda.send_keys(Posadka)
        time.sleep(1.5)
        kuda.send_keys(Visodka)
        time.sleep(1.5)
        kogda.send_keys(Data)



        button = browser.find_element(By.XPATH, '/html/body/div[2]/div[5]/div[3]/div/form/div/div/div[6]/button/span/span[3]')
        button.click()

        time.sleep(1.5)
        skolko3 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[1]')
        skolko3_error = skolko3.text
        skolko = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[1]')
        skolko_error = skolko.text
        skolko2 = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[2]')
        skolko_error2 = skolko2.text
        print(skolko3_error)


        if skolko_error == 'Мы не нашли билеты на поезд на выбранную дату' :
            error_dlg = wx.MessageDialog(self, "Мы не нашли билет на выбранную дату! ", "ERROR", wx.OK_DEFAULT | wx.ICON_ERROR)

            if error_dlg == wx.ID_OK:
                print('OK')
            error_dlg.ShowModal()

        if skolko_error2 == 'Мы не нашли билеты на поезд на выбранную дату' :
            error_dlg = wx.MessageDialog(self, "Мы не нашли билет на выбранную дату! ", "ERROR", wx.OK_DEFAULT | wx.ICON_ERROR)

            if error_dlg == wx.ID_OK:
                print('OK')
            error_dlg.ShowModal()

        if skolko3_error == 'Нет билетов на эту дату':
            error_dlg = wx.MessageDialog(self, "Мы не нашли билет на выбранную дату! ", "ERROR", wx.OK_DEFAULT | wx.ICON_ERROR)

            if error_dlg == wx.ID_OK:
                print('OK')
            error_dlg.ShowModal()



        peresadka_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[3]/div/div[1]/span/span/span')
        peresadka = peresadka_path.text
        price_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/span')
        price = price_path.text

        peresadki_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[3]/div/div[1]/span/span/span')
        peresadki = peresadki_path.text

        vzlet_obh_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div')
        vzlet_obh = vzlet_obh_path.text

        posadka_obh_path = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div')
        posadka_obh = posadka_obh_path.text

        main_dlg = wx.MessageDialog(self, f"Посадка: {vzlet_obh}\nВысодка: {posadka_obh}\nЦена: {price}\nРейс: {peresadka} ", "Info", wx.OK_DEFAULT)

        if main_dlg == wx.ID_OK:
            print('OK')
        main_dlg.ShowModal()

        print(price)
        print(peresadki)
        print(vzlet_obh)
        print(posadka_obh)


app = wx.App()
frame = MyFrame(None, 'Searching')
frame.Show()
app.MainLoop()