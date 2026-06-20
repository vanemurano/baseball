import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP Baseball Manager 2026"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 800
        page.window_center()
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_name = None
        self._txt_result = None
        self._ddAnno = None
        self._txtOutSquadre = None
        self._btnCreaGrafo = None
        self._ddSquadra = None
        self._btnDettagli = None
        self._btnPercorso = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP Baseball Manager 2026", color="blue", size=24)
        # self._page.controls.append(self._title)

        self._txtInAnno = ft.TextField(label="Anno", width=200)
        self._txtInSalario = ft.TextField(label="Salario ($M)", width=200)

        row1 = ft.Row([ft.Container(self._title, width=500),
                       ft.Container(None, width=0),
                       ft.Container(self._txtInAnno, width=250),
                       ft.Container(self._txtInSalario, width=250)], alignment=ft.MainAxisAlignment.CENTER)
        self._txtOutSquadre = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        cont = ft.Container(self._txtOutSquadre, width=300, height= 200, alignment=ft.alignment.top_left, bgcolor="#deeded")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        row2 = ft.Row([cont, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END)

        self._btnConnesse = ft.ElevatedButton(text="Calcola Connesse", on_click=self._controller.handleConnesse)
        self._btnGradoMax = ft.ElevatedButton(text="Grado Massimo", on_click=self._controller.handleGradoMax)
        self._btnDreamTeam = ft.ElevatedButton(text="Dream Team", on_click=self._controller.handleDreamTeam)
        row3 = ft.Row([ft.Container(self._ddSquadra, width=250),
                       ft.Container(self._btnConnesse, width=250),
                       ft.Container(self._btnGradoMax, width=250),
                       ft.Container(self._btnDreamTeam, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)

        for i in range(0,200):
            self._txtOutSquadre.controls.append(ft.Text(f"Squadra {i}"))

        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(ft.Container(self._txt_result, bgcolor="#deeded", height=350))
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()