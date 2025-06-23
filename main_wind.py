import tkinter as tk
from tkinter import ttk, messagebox
import logic

class ClaimsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Система ФОМС")
        self.root.geometry("1200x700")
        self.root.configure(bg="#e9eef4")
        self.root.minsize(1000, 600)

        self.font_main = ("Times New Roman", 12)

        self.setup_ui()
        self.root.mainloop()


    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Навигационная панель
        nav_frame = tk.Frame(self.root, bg="#f4f6f8", width=250)
        nav_frame.grid(row=0, column=0, sticky="nswe")
        nav_frame.grid_propagate(False)
        self.build_nav(nav_frame)

        # Основная область
        content_frame = tk.Frame(self.root, bg="white")
        content_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        content_frame.grid_rowconfigure(2, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        self.content_frame = content_frame

        self.build_content(content_frame)

    def build_nav(self, parent):
        tk.Label(parent, text="Система ФОМС", bg="#f4f6f8", font=(self.font_main[0], 14, "bold"), anchor="w").pack(
            padx=20, pady=(20, 20), anchor="w"
        )

        buttons = [
            ("Статистика мед учреждений", self.handle_static_pharm),
            ("Статистика врачей", self.handle_static_doc),
            ("Лекарства", self.handle_doc),
            ("Анализ диагнозов (МКБ)", self.handle_diagnosis),
            ("Общая динамика", self.handle_overall),
            ("Отчёты (экспорт)", self.create_report)
        ]

        for text, cmd in buttons:
            btn = tk.Button(parent, text=text, bg="#f4f6f8", relief="flat", anchor="w", font=self.font_main, command=cmd)
            btn.pack(fill="x", padx=20, pady=5)

        tk.Button(parent, text="Выйти", bg="#f4f6f8", fg="gray", font=self.font_main,
                  relief="flat", anchor="w", justify="left", command=self.root.quit).pack(padx=20, pady=30, fill="x")

    def build_content(self, parent):
        # Заголовок
        tk.Label(parent, text="Данные", font=(self.font_main[0], 14, "bold"), bg="white").grid(row=0, column=0, sticky="w", pady=(0, 10))


        self.columns = (
            "s_code", "i_doctor", "i_med_entity",
            "s_pin_patient", "i_icd", "i_generic", "d_start"
        )
        self.column_headers = {
            "s_code": "Код рецепта",
            "i_doctor": "Врач",
            "i_med_entity": "Мед. учреждение",
            "s_pin_patient": "Пациент",
            "i_icd": "Диагноз (МКБ)",
            "i_generic": "Лекарство",
            "d_start": "Дата назначения"

        }

        self.tree = ttk.Treeview(parent, columns=self.columns, show="headings")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(self.font_main[0], 12, "bold"))
        style.configure("Treeview", font=self.font_main, rowheight=25)

        for col in self.columns:
            self.tree.heading(col, text=self.column_headers[col])
            self.tree.column(col, anchor="center", width=150)

        self.tree.grid(row=2, column=0, sticky="nswe")

        parent.grid_rowconfigure(2, weight=1)
        parent.grid_columnconfigure(0, weight=1)


    def update_table(self, data):

        if set(self.tree["columns"]) != set(self.columns):
            self.tree.destroy()
            self.tree = ttk.Treeview(self.content_frame, columns=self.columns, show="headings")

            style = ttk.Style()
            style.configure("Treeview.Heading", font=(self.font_main[0], 12, "bold"))
            style.configure("Treeview", font=self.font_main, rowheight=25)

            for col in self.columns:
                self.tree.heading(col, text=self.column_headers[col])
                self.tree.column(col, anchor="center", width=150)

            self.tree.grid(row=2, column=0, sticky="nswe")


        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in data:
            self.tree.insert("", "end", values=row)


    def update_table_simple(self, data, columns):
        self.tree.destroy()
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(self.font_main[0], 12, "bold"))
        style.configure("Treeview", font=self.font_main, rowheight=25)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

        self.tree.grid(row=2, column=0, sticky="nswe")

        for row in data:
            self.tree.insert("", "end", values=row)


    def handle_static_pharm(self):
        data = logic.static_pharm()
        if data:
            self.update_table_simple(data, ["Мед. учреждение", "Всего рецептов", "Уникальных пациентов", "Среднее рецептов на пациента"])
        else:
            self.update_table_simple([], ["Данные отсутствуют"])

    def handle_static_doc(self):
        suspicious, suspicious_summary = logic.static_doc()
        if suspicious:

            self.update_table(suspicious)
        else:
            self.update_table_simple([], ["Нет подозрительных назначений"])

    def handle_doc(self):
        data = logic.doc()
        if data:
            self.update_table_simple(data, ["Лекарство", "Количество назначений"])
        else:
            self.update_table_simple([], ["Данные отсутствуют"])

    def handle_diagnosis(self):
        data = logic.diagnosis_analysis()
        if data:
            self.update_table_simple(data, ["Диагноз (МКБ)", "Количество"])
        else:
            self.update_table_simple([], ["Данные отсутствуют"])

    def handle_overall(self):
        data = logic.overall_dynamics()
        if data:
            self.update_table_simple(data, ["Дата", "Количество рецептов"])
        else:
            self.update_table_simple([], ["Данные отсутствуют"])

    def create_report(self):
        logic.generate_report()

if __name__ == "__main__":
    ClaimsWindow()
