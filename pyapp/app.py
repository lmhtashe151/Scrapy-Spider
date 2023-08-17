import tkinter as tk
from tkinter import ttk
import psycopg2

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product App")

        self.connection = psycopg2.connect(
            host = 'localhost',
            user = 'postgres',
            password = '12345678',
            database = 'chocolate_scraping',
        )
        self.cursor = self.connection.cursor()

        self.tree = ttk.Treeview(root, columns=("Name", "Price", "URL"))
        self.tree.heading("#1", text="Name")
        self.tree.heading("#2", text="Price")
        self.tree.heading("#3", text="URL")
        self.tree.pack()

        self.load_button = tk.Button(root, text="Load Products", command=self.load_products)
        self.load_button.pack()

        self.highest_button = tk.Button(root, text="Highest Price", command=self.show_highest_price)
        self.highest_button.pack()

        self.lowest_button = tk.Button(root, text="Lowest Price", command=self.show_lowest_price)
        self.lowest_button.pack()

    def load_products(self):
        self.cursor.execute("SELECT name, price, url FROM chocolate_products")
        products = self.cursor.fetchall()

        self.tree.delete(*self.tree.get_children())
        for product in products:
            self.tree.insert("", "end", values=product)

    def show_highest_price(self):
        self.cursor.execute("SELECT name, price, url FROM chocolate_products ORDER BY price DESC LIMIT 1")
        product = self.cursor.fetchone()

        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=product)

    def show_lowest_price(self):
        self.cursor.execute("SELECT name, price, url FROM chocolate_products ORDER BY price ASC LIMIT 1")
        product = self.cursor.fetchone()

        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=product)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()
