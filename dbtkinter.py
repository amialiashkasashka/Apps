import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="#FE9191", bd=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        button_insert_data = tk.Button(toolbar, text="Добавить", compound=tk.TOP, bd=0, command=self.open_dialog)
        button_insert_data.pack(side=tk.LEFT)

        button_delete_data = tk.Button(toolbar, text="Удалить", compound=tk.TOP)
        button_delete_data.place(x=100, y=200)
        button_delete_data.pack()

        self.tree = ttk.Treeview(columns=("ID", "col_1", "col_2", "col_3"), height=15, show="headings")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("col_1", width=200, anchor=tk.CENTER)
        self.tree.column("col_2", width=200, anchor=tk.CENTER)
        self.tree.column("col_3", width=200, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("col_1", text="колонка 1")
        self.tree.heading("col_2", text="колонка 2")
        self.tree.heading("col_3", text="колонка 3")

        self.tree.pack()

    def records(self, col_1, col_2, col_3):
        self.db.insert_data(col_1, col_2, col_3)
        self.view_records()

    
    def update_base(self, col_1, col_2, col_3):
        self.db.cur.execute('''UPDATE mydb col_1 = ? col_2 = ? col_3 = ? WHERE ID = ? ''',
                          (col_1, col_2, col_3, self.tree.set(self.tree.selection()[0], "#1")))
        self.db.con.commit()
        self.view_records()

    def view_records(self):
        self.db.cur.execute('''SELECT * FROM mydb''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', "end", values=row)
         for row in self.db.cur.fetchall()]

    def open_dialog(self):
        Child()         


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить в базу")

        self.geometry("420x220+400+300")
        self.resizable(False, False)   

        label_select = tk.Label(self, text="Выбор колонки")
        label_select.place(x=50, y=50)
        label_insert = tk.Label(self, text="Заполняйте")
        label_insert.place(x=50, y=80) 
        label_insert2 = tk.Label(self, text="Заполняйте")
        label_insert2.place(x=50, y=110)

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=200, y=80)
        self.entry_description2 = ttk.Entry(self)
        self.entry_description2.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u"колонка 1", u"колонка 2", u"колонка 3"])
        self.combobox.current(0)
        self.combobox.place(x=200, y=50)

        button_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        button_cancel.place(x=300, y=170)

        button_ok = ttk.Button(self, text="Добавить")
        button_ok.place(x=200, y=170)

        button_ok.bind("<Button-1>", lambda event: self.view.records(
            self.entry_description.get(), self.entry_description2.get(), self.combobox.get()))
        
          

        self.grab_set()
        self.focus_set()    

class DB:
    def __init__(self):
        self.con = sqlite3.connect("dz_db.db")
        self.cur = self.con.cursor()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS mydb(id INTEGER PRIMARY KEY AUTOINCREMENT, col_1 TEXT, col_2 TEXT, col_3 TEXT)")
        self.con.commit()

    def insert_data(self, col_1, col_2, col_3):
        self.cur.execute(
            """INSERT INTO mydb(col_1, col_2, col_3) VALUES(?, ?, ?)""", (col_1, col_2, col_3,))
        self.con.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("MyDB")
    root.geometry("650x450+300+200")
    root.resizable(False, False)
    root.mainloop()
