import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from DB import DB


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="images/add.png")
        btn_open_dialog = tk.Button(toolbar, text='Dodaj pozycję', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file="images/edit.png")
        btn_edit_dialog = tk.Button(toolbar, text='Edytuj pozycję', command=self.open_update_dialog, bg='#d7d8e0',
                                    bd=0, compound=tk.TOP, image=self.update_img)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file="images/delete.png")
        btn_delete = tk.Button(toolbar, text='Usuń pozycję', command=self.delete_records, bg='#d7d8e0',
                               bd=0, compound=tk.TOP, image=self.delete_img)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="images/search.png")
        btn_search = tk.Button(toolbar, text='Wyszukaj', command=self.open_search_dialog, bg='#d7d8e0',
                               bd=0, compound=tk.TOP, image=self.search_img)
        btn_search.pack(side=tk.LEFT)

        self.sort_img = tk.PhotoImage(file="images/sort.png")
        btn_sort = tk.Button(toolbar, text='Sortuj', command=self.view_sort_records, bg='#d7d8e0',
                             bd=0, compound=tk.TOP, image=self.sort_img)
        btn_sort.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file="images/refresh.png")
        btn_refresh = tk.Button(toolbar, text='Odśwież', command=self.view_records, bg='#d7d8e0',
                                bd=0, compound=tk.TOP, image=self.refresh_img)
        btn_refresh.pack(side=tk.RIGHT)

        self.stat_img = tk.PhotoImage(file="images/stat.png")
        btn_stat = tk.Button(toolbar, text='Statystyka', command=self.open_statistic_dialog, bg='#d7d8e0',
                                bd=0, compound=tk.TOP, image=self.stat_img)
        btn_stat.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total', 'dates'),
                                 height=15, show='headings')
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("description", width=250, anchor=tk.CENTER)
        self.tree.column("costs", width=150, anchor=tk.CENTER)
        self.tree.column("total", width=150, anchor=tk.CENTER)
        self.tree.column("dates", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("description", text='Nazwa')
        self.tree.heading("costs", text='Dochód/Wydatek')
        self.tree.heading("total", text='Ilość')
        self.tree.heading("dates", text='Data')

        self.tree.pack()

    def records(self, description, costs, total, dates):
        self.db.insert_data(description, costs, total, dates)
        self.view_records()

    def update_record(self, description, costs, total, dates):
        self.db.c.execute('''UPDATE finance SET description=?, costs=?, total=?, dates=? WHERE ID=?''',
                          (description, costs, total, dates, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def view_sort_records(self):
        self.db.c.execute('''SELECT * FROM finance order by total desc''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM finance WHERE id=?''', (self.tree.set(selection_item, '#1'),))

        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM finance WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        curItem = self.tree.item(self.tree.focus())
        # get a description, amount, date from table
        try:
            Update(curItem['values'][1], curItem['values'][2], curItem['values'][3], curItem['values'][4])
        except IndexError:
            messagebox.showerror("Pomyłka", "Wybierz jedną pozycję")

    def open_search_dialog(self):
        Search()

    def open_statistic_dialog(self):
        Statistic()

class Statistic(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.entry_date2 = ttk.Entry(self)
        self.entry_date1 = ttk.Entry(self)
        self.view = app
        self.db = db
        self.init_statisic()
        self.view_records_expenses()
        self.view_records_income()


    def check_data(self):
        form_date = self.entry_date1.get()
        form_date2 = self.entry_date2.get()
        try:
            year, month, day = map(int, form_date.split('-'))
            year, month, day = map(int, form_date2.split('-'))
        except:
            messagebox.showinfo("Pomyłka", "Niepoprawnie wrowadzona/-e data/-y")
            self.lift()

    def view_select_records(self):
        self.view_records_expenses()
        self.view_records_income()
        self.check_data()

        label_sum_expenses = ttk.Label(self, text='Kwota:')
        label_sum_expenses.config(font=10)
        label_sum_expenses.place(x=50, y=325)

        label_sum = ttk.Label(self, text=self.count_sum_expenses())
        label_sum.config(font=10)
        label_sum.place(x=200, y=325)

        label_sum_incomes = ttk.Label(self, text='Kwota:')
        label_sum_incomes.config(font=10)
        label_sum_incomes.place(x=355, y=325)

        label_sum2 = ttk.Label(self, text=self.count_sum_income())
        label_sum2.config(font=10)
        label_sum2.place(x=505, y=325)

        label_total = tk.Label(self, text='Pozostała suma:')
        label_total.config(fg="#ff1100")
        label_total.config(font=10)
        label_total.place(x=50, y=360)


        label_sum3 = tk.Label(self, text=self.total_count_sum())
        label_sum3.config(fg="#ff1100")
        label_sum3.config(font=10)
        label_sum3.place(x=200, y=360)


    def init_statisic(self):
        self.title('Statystyka')
        self.geometry('600x420+400+250')
        self.resizable(False, False)

        label_okres = ttk.Label(self, text='Okres')
        label_okres.config(font=10)
        label_okres.place(x=50, y=40)

        self.entry_date1.place(x=50, y=80)
        ods = ttk.Button(self, text="Odśwież", command=self.view_select_records)
        ods.place(x=450, y=360)

        label_okres = ttk.Label(self, text='-')
        label_okres.place(x=183, y=80)

        self.entry_date2.place(x=200, y=80)

        self.tree = ttk.Treeview(self, columns=('description', 'total'),
                                 height=8, show='headings')
        self.tree2 = ttk.Treeview(self, columns=('description', 'total'),
                                 height=8, show='headings')

        self.tree.column("description", width=150, anchor=tk.CENTER)
        self.tree.column("total", width=150, anchor=tk.CENTER)
        self.tree.heading("description", text='Wydatek')
        self.tree.heading("total", text='Ilość')

        self.tree2.column("description", width=150, anchor=tk.CENTER)
        self.tree2.column("total", width=150, anchor=tk.CENTER)
        self.tree2.heading("description", text='Dochód')
        self.tree2.heading("total", text='Ilość')

        self.tree.pack(side='left')
        self.tree2.pack(side='left')

    def total_count_sum(self):
        return self.count_sum_expenses() + self.count_sum_income()

    def count_sum_expenses(self):
        sum_expenses = 0
        for child in self.tree.get_children():
            sum_expenses += float(self.tree.item(child)["values"][1])
        return sum_expenses

    def count_sum_income(self):
        sum_incomes = 0
        for child in self.tree2.get_children():
            sum_incomes += float(self.tree2.item(child)["values"][1])
        return sum_incomes

    def view_records_expenses(self):
        self.db.c.execute('''SELECT description, total FROM finance WHERE (dates BETWEEN ? AND ?) AND costs="Wydatek"''', (self.entry_date1.get(), self.entry_date2.get()))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


    def view_records_income(self):
        self.db.c.execute('''SELECT description, total FROM finance WHERE (dates BETWEEN ? AND ?) AND costs="Dochód"''', (self.entry_date1.get(), self.entry_date2.get()))
        [self.tree2.delete(i) for i in self.tree2.get_children()]
        [self.tree2.insert('', 'end', values=row) for row in self.db.c.fetchall()]

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Dodawanie')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Nazwa:')
        label_description.place(x=50, y=50)
        label_select = tk.Label(self, text='Dochód/Wydatek:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Ilość:')
        label_sum.place(x=50, y=110)
        label_date = tk.Label(self, text='Data:')
        label_date.place(x=50, y=140)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u"Dochód", u"Wydatek"])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        self.entry_date = ttk.Entry(self)
        self.entry_date.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text='Zamknij', command=self.destroy)
        btn_cancel.place(x=300, y=180)

        self.btn_ok = ttk.Button(self, text='Dodaj', command=self.check_data)
        self.btn_ok.place(x=220, y=180)


        self.grab_set()
        self.focus_set()


    def check_data(self):
        form_date = self.entry_date.get()
        ilosc = self.entry_money.get()
        try:
            day, month, year = map(int, form_date.split('-'))
            ilosc = float(ilosc)
            self.view.records(self.entry_description.get(),
                              self.combobox.get(),
                              self.entry_money.get(),
                              self.entry_date.get())
            self.destroy()
        except:
            messagebox.showinfo("Pomyłka", "Niepoprawnie wrowadzona data")

class Update(Child):
    def __init__(self, desc, costs, money, date):
        super().__init__()
        self.init_edit(desc, costs, money, date)
        self.view = app
        self.desc = desc
        self.money = money
        self.date = date

    def init_edit(self, desc, costs, money, date):
        self.title('Edycja')

        self.btn_ok.destroy()
        self.entry_description.destroy()
        self.entry_money.destroy()
        self.entry_date.destroy()

        self.v = tk.StringVar(self, value=desc)
        self.entry_edit_description = ttk.Entry(self, textvariable=self.v)
        self.entry_edit_description.place(x=200, y=50)

        self.a = tk.StringVar(self, value=money)
        self.entry_edit_money = ttk.Entry(self, textvariable=self.a)
        self.entry_edit_money.place(x=200, y=110)


        self.r = tk.StringVar(self, value=date)
        self.entry_edit_date = ttk.Entry(self, textvariable=self.r)

        self.entry_edit_date.place(x=200, y=140)

        self.c = tk.StringVar(self, value=costs)

        btn_edit = ttk.Button(self, text='Edytuj', command=self.check_edit_data)
        btn_edit.place(x=220, y=180)


    def check_edit_data(self):
        form_date = self.entry_edit_date.get()
        ilosc = self.entry_edit_money.get()
        try:
            day, month, year = map(int, form_date.split('-'))
            ilosc = float(ilosc)
            self.view.update_record(self.entry_edit_description.get(),
                                    self.combobox.get(),
                                    self.entry_edit_money.get(),
                                    self.entry_edit_date.get())
            self.destroy()
        except:
            messagebox.showinfo("Pomyłka", "Niepoprawnie wrowadzona data")


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title("Wyszukaj")
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Szukaj')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Zamknij', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Szukaj')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


def help_info():
    messagebox.showinfo("Informacja", "<Dodaj pozycję> - dodaje utworzoną przez ciebie pozycję do tabeli"
                                      "\n<Edytuj pozycję> - edytuje wybraną pozycję"
                                      "\n<Usuń pozycję> - usuwa wybraną pozucję z tabeli"
                                      "\n<Wyszukaj> - wyszukuje w tabeli pozycji według wprowadzonej nazwy pozycji"
                                      "\n<Sortuj> - sortuje pozycji rosnąco/malejąco według kwoty"
                                      "\n<Odśwież> - odświeża tabelę po sortowaniu/wyszukiwaniu"
                                      "\n<Statystyka> - generuje statystykę dochodów i wydatków za określony czas")


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Księgowość")
    root.geometry("735x450+300+200")
    root.resizable(False, False)
    mainMenu = tk.Menu()
    root.config(menu=mainMenu)
    fileMenu = tk.Menu(mainMenu, tearoff=False)
    mainMenu.add_cascade(label='Menu', menu=fileMenu)

    fileMenu.add_command(label='Pomoc', command=help_info)
    root.mainloop()
