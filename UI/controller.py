import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        x=self._view._txtInGoal.value
        if x=="":
            self._view._txt_result.controls.append(
                ft.Text("Inserire numero minimo di goal!", color="red")
            )
            self._view.update_page()
            return
        try:
            floatX=float(x)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Il numero di goal deve essere un decimale positivo!", color="red")
            )
            self._view.update_page()
            return
        if floatX<0:
            self._view._txt_result.controls.append(
                ft.Text("Il numero di goal deve essere un decimale positivo!", color="red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(floatX)
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo creato, con {self._model.getNNodes()} vertici e {self._model.getNEdges()} archi")
        )
        self._view.update_page()

    def handleTopPlayer(self, e):
        if self._model.getNNodes()==0:
            self._view._txt_result.controls.append(
                ft.Text("Creare prima il grafo!", color="red")
            )
            self._view.update_page()
            return
        self._view._txt_result.controls.append(
            ft.Text(f"Top player: {self._model.getTopPlayer()}\n"
                    f"Avversari battuti:")
        )
        for avv, peso in self._model.getAvversari():
            self._view._txt_result.controls.append(
                ft.Text(f"{avv} | {peso}")
            )
        self._view.update_page()

    def handleDreamTeam(self, e):
        if self._model.getNNodes() == 0:
            self._view._txt_result.controls.append(
                ft.Text("Creare prima il grafo!", color="red")
            )
            self._view.update_page()
            return
        k = self._view._txtInK.value
        if k == "":
            self._view._txt_result.controls.append(
                ft.Text("Inserire numero di giocatori!", color="red")
            )
            self._view.update_page()
            return
        try:
            intK = float(k)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Il numero deve essere un intero positivo!", color="red")
            )
            self._view.update_page()
            return
        if intK < 0:
            self._view._txt_result.controls.append(
                ft.Text("Il numero deve essere un intero positivo!", color="red")
            )
            self._view.update_page()
            return
        team, gradoOtt=self._model.dreamTeam(intK)
        self._view._txt_result.controls.append(
            ft.Text(f"Dream team (grado di ottimalità {gradoOtt}):")
        )
        for player in team:
            self._view._txt_result.controls.append(
                ft.Text(player)
            )
        self._view.update_page()