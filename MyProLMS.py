import tkinter as tk
from tkinter import messagebox, ttk

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("700x400")

        # Book data storage: list of dicts
        self.books = []
        self.selected_index = None

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Labels and Entry fields
        tk.Label(self.root, text="Title").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.title_text = tk.StringVar()
        self.title_entry = tk.Entry(self.root, textvariable=self.title_text)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Author").grid(row=0, column=2, padx=10, pady=5, sticky='w')
        self.author_text = tk.StringVar()
        self.author_entry = tk.Entry(self.root, textvariable=self.author_text)
        self.author_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(self.root, text="Year").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.year_text = tk.StringVar()
        self.year_entry = tk.Entry(self.root, textvariable=self.year_text)
        self.year_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="ISBN").grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.isbn_text = tk.StringVar()
        self.isbn_entry = tk.Entry(self.root, textvariable=self.isbn_text)
        self.isbn_entry.grid(row=1, column=3, padx=10, pady=5)

        # Buttons
        tk.Button(self.root, text="Add Book", width=12, command=self.add_book).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Update Book", width=12, command=self.update_book).grid(row=2, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Delete Book", width=12, command=self.delete_book).grid(row=2, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Clear Fields", width=12, command=self.clear_fields).grid(row=2, column=3, padx=10, pady=10)

        # Book list display using Treeview
        columns = ("Title", "Author", "Year", "ISBN")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=3, column=4, sticky='ns')

        # Bind select event
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Configure grid weights for resizing
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

    def add_book(self):
        title = self.title_text.get().strip()
        author = self.author_text.get().strip()
        year = self.year_text.get().strip()
        isbn = self.isbn_text.get().strip()

        if not title or not author or not year or not isbn:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        # Add book to list
        self.books.append({"Title": title, "Author": author, "Year": year, "ISBN": isbn})
        self.refresh_tree()
        self.clear_fields()

    def update_book(self):
        if self.selected_index is None:
            messagebox.showwarning("Selection Error", "No book selected to update")
            return

        title = self.title_text.get().strip()
        author = self.author_text.get().strip()
        year = self.year_text.get().strip()
        isbn = self.isbn_text.get().strip()

        if not title or not author or not year or not isbn:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        # Update selected book
        self.books[self.selected_index] = {"Title": title, "Author": author, "Year": year, "ISBN": isbn}
        self.refresh_tree()
        self.clear_fields()

    def delete_book(self):
        if self.selected_index is None:
            messagebox.showwarning("Selection Error", "No book selected to delete")
            return

        del self.books[self.selected_index]
        self.refresh_tree()
        self.clear_fields()

    def clear_fields(self):
        self.title_text.set("")
        self.author_text.set("")
        self.year_text.set("")
        self.isbn_text.set("")
        self.selected_index = None
        self.tree.selection_remove(self.tree.selection())

    def refresh_tree(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert all books
        for book in self.books:
            self.tree.insert('', tk.END, values=(book["Title"], book["Author"], book["Year"], book["ISBN"]))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            self.selected_index = index
            book = self.books[index]
            self.title_text.set(book["Title"])
            self.author_text.set(book["Author"])
            self.year_text.set(book["Year"])
            self.isbn_text.set(book["ISBN"])
        else:
            self.selected_index = None

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
