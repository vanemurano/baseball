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

        self._txtInGoal = ft.TextField(label="Goal fatti", width=200)
        self._txtInK = ft.TextField(label="Giocatori (k)", width=200)

        row1=ft.Row([self._title],
                    alignment=ft.MainAxisAlignment.CENTER)
        row2 = ft.Row([ft.Container(None, width=0),
                       ft.Container(self._txtInGoal, width=250),
                       ft.Container(self._txtInK, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._btnTopPlayer = ft.ElevatedButton(text="Top Player", on_click=self._controller.handleTopPlayer)
        self._btnDreamTeam = ft.ElevatedButton(text="Dream Team", on_click=self._controller.handleDreamTeam)
        row3 = ft.Row([ft.Container(self._btnCreaGrafo, width=250),
                       ft.Container(self._btnTopPlayer, width=250),
                       ft.Container(self._btnDreamTeam, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)

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