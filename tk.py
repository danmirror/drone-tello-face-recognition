import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.user_input = tk.Entry(self)
        self.user_input.pack()

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_data)
        self.submit_button.pack()

    def submit_data(self):
        user_data = self.user_input.get()
        print("User data:", user_data)

app = App()
app.mainloop()
