import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder

import matplotlib.pyplot as plt 
import numpy as np

import mysql.connector
#create DB called cdbs
#CHANGE USER AND PASSWD for final product!!!!!! requires DB with 6 tables firstname, lastname, dob, email, phone, notetable
mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root", 
    passwd = "",
    database = "cdbs"
)

mycursor = mydb.cursor()

#change password for final product!!!
username = "Misti"
password = "1234"
class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text = "Username:"))

        self.username = TextInput(multiline = False, password = True)
        self.add_widget(self.username)

        self.add_widget(Label(text = "Password:"))

        self.password = TextInput(multiline = False, password = True)
        self.add_widget(self.password)

        self.button_login = Button(text = "Log In")
        self.add_widget(self.button_login)
        self.button_login.bind(on_press = self.func_login)
#------------------------Pages---------------------------
    def page_home(self, instance):
        self.clear_widgets()
        self.cols = 1

        self.button_clients = Button(text = "Clients")
        self.add_widget(self.button_clients)
        self.button_clients.bind(on_press = self.func_page_clients)

    def page_clients(self, instance):
        self.clear_widgets()
        self.cols = 1

        self.button_existing_clients = Button(text = "Existing Clients")
        self.add_widget(self.button_existing_clients)
        self.button_existing_clients.bind(on_press = self.func_page_existing_clients)

        self.button_create_client = Button(text = "Create New Client")
        self.add_widget(self.button_create_client)
        self.button_create_client.bind(on_press = self.func_create_client)
    
    def page_new_client(self, instance):
        self.clear_widgets()
        self.cols = 2

        self.add_widget(Label(text = "First Name:"))
        
        self.new_client_first_name = TextInput(multiline = False)
        self.add_widget(self.new_client_first_name)

        self.add_widget(Label(text = "Last Name:"))

        self.new_client_last_name = TextInput(multiline = False)
        self.add_widget(self.new_client_last_name)

        self.add_widget(Label(text = "Date of Birth (YYYY-MM-DD"))

        self.new_client_dob = TextInput(multiline = False)
        self.add_widget(self.new_client_dob)

        self.add_widget(Label(text = "Email"))

        self.new_client_email = TextInput(multiline = False)
        self.add_widget(self.new_client_email)

        self.add_widget(Label(text = "Phone"))

        self.new_client_phone = TextInput(multiline = False)
        self.add_widget(self.new_client_phone)

        self.button_new_client_submit = Button(text = "Submit")
        self.add_widget(self.button_new_client_submit)
        self.button_new_client_submit.bind(on_press = self.func_new_client_submit)

        self.button_new_client_cancel = Button(text = "Cancel")
        self.add_widget(self.button_new_client_cancel)
        self.button_new_client_cancel.bind(on_press = self.func_page_clients)
    def page_existing_clients(self, instance):
        self.clear_widgets()
        self.cols = 2

        self.add_widget(Label(text = "Last Name:"))

        self.search_last_name = TextInput(multiline = False)
        self.add_widget(self.search_last_name)

        self.button_search_last_name = Button(text= "Search")
        self.add_widget(self.button_search_last_name)
        self.button_search_last_name.bind(on_press = self.func_search_last_name)

#------------------------Functions-----------------------
    def func_login(self, instance):
        if self.username.text == username and self.password.text == password:
            self.page_home(instance)

    def func_page_clients(self, instance):
        self.page_clients(instance)

    def func_create_client(self, instance):
        self.page_new_client(instance)
    
    def func_new_client_submit(self, instance):
        self.new_client_notetable = str(self.new_client_first_name.text) + str(self.new_client_last_name.text) + str(self.new_client_dob.text)

        sql = "INSERT INTO clients (firstname, lastname, dob, email, phone, notetable) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (self.new_client_first_name.text, self.new_client_last_name.text, self.new_client_dob.text, self.new_client_email.text, self.new_client_phone.text, self.new_client_notetable)

        mycursor.execute(sql, val)
        mydb.commit()

        self.page_clients(instance)
    def func_page_existing_clients(self, instance):
        self.page_existing_clients(instance)
    
    def func_search_last_name(self, instance):
        mycursor.execute("SELECT * FROM clients WHERE", (self.search_last_name.text))
        myresult = mycursor.fetchall()
        self.clear_widgets()
        self.cols = 1
        for x in myresult:
            self.add_widget(Label(x))
#--------------------------------------------------------
class MyClientDatabase(App):
    def build(self):
        return LoginScreen()
MyClientDatabase().run()