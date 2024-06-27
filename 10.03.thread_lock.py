# -*- coding: utf-8 -*-
from threading import Thread, Lock
from time import sleep


class BankAccount():

    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def deposit(self, money):
        self.amount += money

    def wdr(self, money):
        self.amount -= money


def dep_task(account, amount):
    global x  # Моя кубышка — имитация общего ресурса
    for _ in range(5):
        with lock_dep:
            x -= amount * 0.01  # Достаём немного и из кубышки, чтобы положить на депозит. Имитация общего ресурса
            account.deposit(amount)
            print(f'Account {account.account}. Deposited {amount:7.2f}, balance {account.amount:8.2f}. В моей кубышке: {x:5.2f}')
        sleep(1)  # Для красоты, чтобы потоки перемешались


def wdr_task(account, amount):
    global x  # Моя кубышка — имитация общего ресурса
    for _ in range(5):
        with lock_wdr:
            x += amount * 0.01   # Кладём в кубышку, из доходов в банке. Имитация общего ресурса
            account.wdr(amount)
            print(f'Account {account.account}. Withdrew  {amount:7.2f}, balance {account.amount:8.2f}. В моей кубышке: {x:5.2f}')
        sleep(1)  # Для красоты, чтобы потоки перемешались


acc1 = BankAccount("2024abcd", 1000)
x = 10  # Кубышка — имитация общего ресурса
print(f'Created account {acc1.account}. Balance = {acc1.amount:8.2f}')
print(f'В моей кубышке: {x:5.2f}')
lock_dep = Lock()  # Для депозитов
lock_wdr = Lock()  # Для снятий
t_dep = Thread(target=dep_task, args=(acc1, 100))
t_wdr = Thread(target=wdr_task, args=(acc1, 150))

t_dep.start()
sleep(0.1)
t_wdr.start()

t_dep.join()
t_wdr.join()
print('--------- The End ---------')
