import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import re

class databaseHandler:
    @staticmethod
    def koneksi_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="manajemen_toko"
        )
    
    @staticmethod
    def fetch_db(sort_by="waktu_pembuatan DESC"):
        conn = databaseHandler.koneksi_db()
        cursor = conn.cursor()
        try:
            query = (f"""SELECT m.ID_transaksi, m.ID_PRODUK, p.nama_produk,
                                p.harga_produk, m.jumlah_barang, m.total_harga, m.waktu_pembuatan
                           FROM catatan_transaksi m
                           JOIN barang_product p ON m.ID_PRODUK = p.ID_PRODUK
                           ORDER BY {sort_by}
                     """)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("konfigurasi database Error ", f"Error: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def fetch_products():
        conn = databaseHandler.koneksi_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_PRODUK, nama_produk, harga_produk FROM barang_product")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("konfigurasi database Error ", f"Error: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_transaction(ID_PRODUK, jumlah_barang):
        conn = databaseHandler.koneksi_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT harga_produk FROM barang_product WHERE ID_PRODUK = %s", (ID_PRODUK,))
            harga_produk = cursor.fetchone()[0]
            total_harga = harga_produk * jumlah_barang
            cursor.execute(
                "INSERT INTO catatan_transaksi (ID_PRODUK, jumlah_barang, total_harga) VALUES (%s, %s, %s)",
                (ID_PRODUK, jumlah_barang, total_harga)
            )
            conn.commit()
            messagebox.showinfo("Success", "Transaction added successfully")
        except Exception as e:
            messagebox.showerror("konfigurasi database Error ", f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def add_product(nama_produk, harga_produk):
        conn = databaseHandler.koneksi_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO barang_product (nama_produk, harga_produk) VALUES (%s, %s)",
                (nama_produk, harga_produk)
            )
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully")
        except Exception as e:
            messagebox.showerror("konfigurasi database Error ", f"Error: {str(e)}")
        finally:
            cursor.close()
            conn.close()

class mainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Program Manajemen Toko Sederhana")
        self.geometry("853x480")
        self.setup_gui_and_bg()
        self.create_widgets()
        self.bind("<Configure>", self.resize_bg)

    def setup_gui_and_bg(self):
        self.bg_image = Image.open("asset\\oshi.jpg")
        self.bg_image = self.bg_image.convert("RGBA")
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_image_tk)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()

    def resize_bg(self, event):
        new_width = event.width
        new_height = event.height
        self.bg_image_resized = self.bg_image.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image_tk_resized = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label.config(image=self.bg_image_tk_resized)
        self.bg_label.image = self.bg_image_tk_resized

    def create_widgets(self):
        # Create a frame for the product selection and transaction addition
        self.product_frame = tk.Frame(self, bg=self.cget("background"))
        self.product_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.product_label = tk.Label(self.product_frame, text="Select Product:", bg=self.cget("background"))
        self.product_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.product_combobox = ttk.Combobox(self.product_frame)
        self.product_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.quantity_label = tk.Label(self.product_frame, text="Enter Quantity:", bg=self.cget("background"))
        self.quantity_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.quantity_entry = tk.Entry(self.product_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.add_button = tk.Button(self.product_frame, text="Add Transaction", command=self.add_transaction, bg=self.cget("background"))
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.show_transactions_button = tk.Button(self.product_frame, text="Show Transactions", command=self.show_transactions, bg=self.cget("background"))
        self.show_transactions_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Create a frame for adding new products
        self.new_product_frame = tk.Frame(self, bg=self.cget("background"))
        self.new_product_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.add_product_label = tk.Label(self.new_product_frame, text="Add New Product:", bg=self.cget("background"))
        self.add_product_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.new_product_name_label = tk.Label(self.new_product_frame, text="Product Name:", bg=self.cget("background"))
        self.new_product_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.new_product_name_entry = tk.Entry(self.new_product_frame)
        self.new_product_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.new_product_price_label = tk.Label(self.new_product_frame, text="Product Price:", bg=self.cget("background"))
        self.new_product_price_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.new_product_price_entry = tk.Entry(self.new_product_frame)
        self.new_product_price_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.add_product_button = tk.Button(self.new_product_frame, text="Add Product", command=self.add_product, bg=self.cget("background"))
        self.add_product_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Configure Treeview style
        style = ttk.Style()
        style.configure("mystyle.Treeview", 
                        background=self.cget("background"), 
                        fieldbackground=self.cget("background"), 
                        borderwidth=0)
        style.configure("mystyle.Treeview.Heading")

        # Create a frame for the transactions table
        self.transactions_frame = tk.Frame(self, bg=self.cget("background"))
        self.transactions_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        self.transactions_tree = ttk.Treeview(self.transactions_frame, columns=("ID", "Product", "Quantity", "Total Price", "Date"), show='headings', style="mystyle.Treeview")
        self.transactions_tree.heading("ID", text="ID")
        self.transactions_tree.heading("Product", text="Product")
        self.transactions_tree.heading("Quantity", text="Quantity")
        self.transactions_tree.heading("Total Price", text="Total Price")
        self.transactions_tree.heading("Date", text="Date")

        # Set column widths and stretch options
        self.transactions_tree.column("ID", width=50, stretch=tk.YES)
        self.transactions_tree.column("Product", width=150, stretch=tk.YES)
        self.transactions_tree.column("Quantity", width=100, stretch=tk.YES)
        self.transactions_tree.column("Total Price", width=100, stretch=tk.YES)
        self.transactions_tree.column("Date", width=150, stretch=tk.YES)

        self.transactions_tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.load_products()

    def load_products(self):
        products = databaseHandler.fetch_products()
        self.product_combobox['values'] = [f"{p[1]} (ID: {p[0]}, Price: {p[2]})" for p in products]

    def add_transaction(self):
        selected_product = self.product_combobox.get()
        if not selected_product:
            messagebox.showerror("Input Error", "Please select a product")
            return

        try:
            ID_PRODUK = int(re.search(r'ID: (\d+)', selected_product).group(1))
            jumlah_barang = int(self.quantity_entry.get())
            databaseHandler.add_transaction(ID_PRODUK, jumlah_barang)
            self.show_transactions()  # Refresh the transactions table
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")

    def add_product(self):
        nama_produk = self.new_product_name_entry.get()
        harga_produk = self.new_product_price_entry.get()
        if not nama_produk or not harga_produk:
            messagebox.showerror("Input Error", "Please enter both product name and price")
            return

        try:
            harga_produk = float(harga_produk)
            databaseHandler.add_product(nama_produk, harga_produk)
            self.load_products()  # Refresh the product list
        except ValueError:
            messagebox.showerror("Input Error", "Invalid price format")

    def show_transactions(self):
        for row in self.transactions_tree.get_children():
            self.transactions_tree.delete(row)

        transactions = databaseHandler.fetch_db()
        for transaction in transactions:
            self.transactions_tree.insert("", "end", values=(
                transaction[0], transaction[2], transaction[4], transaction[5], transaction[6]
            ))

if __name__ == "__main__":
    app = mainApp()
    app.mainloop()