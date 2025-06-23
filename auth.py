import tkinter as tk
from tkinter import messagebox
import main_wind
import logic_auth

class AuthWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ФОМС — Вход")
        self.root.configure(bg="#e9eef4")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)

        self.build_interface()
        self.root.mainloop()

    def build_interface(self):
        self.container = tk.Frame(self.root, bg="white")
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.8)
        self.container.pack_propagate(0)

        self.login_frame = self.create_login_frame()
        self.register_frame = self.create_register_frame()

        self.login_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def create_login_frame(self):
        frame = tk.Frame(self.container, bg="white")

        tk.Label(frame, text="Система ФОМС", font=("Times New Roman", 18, "bold"), bg="white").pack(pady=30)

        tk.Label(frame, text="Никнейм", font=("Times New Roman", 14), bg="white", anchor="w").pack(fill="x", padx=50)
        self.username_entry = tk.Entry(frame, font=("Times New Roman", 14), bg="#f5f5f5", relief="flat")
        self.username_entry.pack(fill="x", padx=50, pady=(0, 15), ipady=6)

        tk.Label(frame, text="Пароль", font=("Times New Roman", 14), bg="white", anchor="w").pack(fill="x", padx=50)
        self.password_entry = tk.Entry(frame, font=("Times New Roman", 14), bg="#f5f5f5", relief="flat", show="*")
        self.password_entry.pack(fill="x", padx=50, pady=(0, 15), ipady=6)

        tk.Button(frame, text="Войти", bg="#007bff", fg="white", font=("Times New Roman", 15, "bold"),
                  relief="flat", cursor="hand2", command=self.check_login).pack(pady=10, ipadx=100, ipady=6)

        tk.Label(frame, text="Нет аккаунта?", font=("Times New Roman", 13), bg="white").pack()
        signup_link = tk.Label(frame, text="Зарегистрироваться", font=("Times New Roman", 13),
                               fg="blue", bg="white", cursor="hand2")
        signup_link.pack()
        signup_link.bind("<Button-1>", self.animate_to_register)

        return frame

    def create_register_frame(self):
        frame = tk.Frame(self.container, bg="white")

        tk.Label(frame, text="Регистрация в ФОМС", font=("Times New Roman", 15, "bold"), bg="white").pack(pady=30)

        tk.Label(frame, text="ФИО", font=("Times New Roman", 14), bg="white", anchor="w").pack(fill="x", padx=50)
        self.fullname_entry = tk.Entry(frame, font=("Times New Roman", 14), bg="#f5f5f5", relief="flat")
        self.fullname_entry.pack(fill="x", padx=50, pady=(0, 10), ipady=6)

        tk.Label(frame, text="Придумайте ник", font=("Times New Roman", 14), bg="white", anchor="w").pack(fill="x", padx=50)
        self.username_reg_entry = tk.Entry(frame, font=("Times New Roman", 14), bg="#f5f5f5", relief="flat")
        self.username_reg_entry.pack(fill="x", padx=50, pady=(0, 10), ipady=6)

        tk.Label(frame, text="Пароль", font=("Times New Roman", 14), bg="white", anchor="w").pack(fill="x", padx=50)
        self.password_reg_entry = tk.Entry(frame, font=("Times New Roman", 14), bg="#f5f5f5", relief="flat", show="*")
        self.password_reg_entry.pack(fill="x", padx=50, pady=(0, 10), ipady=6)

        tk.Button(frame, text="Зарегистрироваться", bg="#28a745", fg="white",
                  font=("Times New Roman", 15, "bold"), relief="flat", cursor="hand2",
                  command=self.register_user).pack(pady=10, ipadx=80, ipady=6)

        back_link = tk.Label(frame, text="← Назад к входу", font=("Times New Roman", 13), fg="blue", bg="white", cursor="hand2")
        back_link.pack()
        back_link.bind("<Button-1>", self.animate_to_login)

        return frame

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if logic_auth.verify_login(username, password):
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            self.root.destroy()
            main_wind.ClaimsWindow()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def register_user(self):
        fullname = self.fullname_entry.get()
        username = self.username_reg_entry.get()
        password = self.password_reg_entry.get()

        if not fullname or not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        success, message = logic_auth.register_user(fullname, None, username, password)

        if success:
            messagebox.showinfo("Успех", message)
            self.animate_to_login()
        else:
            messagebox.showerror("Ошибка", message)

    def animate_to_register(self, event=None):
        self.slide_frames(self.login_frame, self.register_frame, direction="left")

    def animate_to_login(self, event=None):
        self.slide_frames(self.register_frame, self.login_frame, direction="right")

    def slide_frames(self, from_frame, to_frame, direction="left"):
        container_width = self.container.winfo_width()
        from_x = 0
        to_x = -container_width if direction == "left" else container_width
        step = -20 if direction == "left" else 20

        def animate():
            nonlocal from_x
            if (direction == "left" and from_x > to_x) or (direction == "right" and from_x < to_x):
                from_x += step
                from_frame.place(x=from_x, y=0)
                to_frame.place(x=from_x + container_width if direction == "left" else from_x - container_width, y=0)
                self.root.after(10, animate)
            else:
                from_frame.place_forget()
                to_frame.place(x=0, y=0, relwidth=1, relheight=1)

        animate()


if __name__ == "__main__":
    AuthWindow()
