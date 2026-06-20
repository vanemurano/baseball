import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceTeam = None

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        if self._view._txtInAnno.value=="":
            self._view._txt_result.controls.append(
                ft.Text(f"Inserire prima un anno!", color="red")
            )
            self._view.update_page()
            return
        if self._view._txtInSalario.value=="":
            self._view._txt_result.controls.append(
                ft.Text(f"Inserire prima un salario!", color="red")
            )
            self._view.update_page()
            return
        try:
            anno=int(self._view._txtInAnno.value)
            salarioM=int(self._view._txtInSalario.value)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text(f"Anno e salario devono essere numeri interi!", color="red")
            )
            self._view.update_page()
            return
        if not self._model.controlloAnni(anno):
            self._view._txt_result.controls.append(
                ft.Text(f"Inserire anno compreso tra 1871 e 2019", color="red")
            )
            self._view.update_page()
            return
        self._model.creaGrafo(anno, salarioM)
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo creato\n"
                    f"Ci sono {self._model.getNNodi()} nodi\n"
                    f"Ci sono {self._model.getNArchi()} archi")
        )
        self._view.update_page()

    def handleConnesse(self, e):
        if not self._model.getNNodi():
            self._view._txt_result.controls.append(
                ft.Text(f"Creare prima il grafo!", color="red")
            )
            self._view.update_page()
            return
        self._view._txt_result.controls.append(
            ft.Text(f"Ci sono {self._model.getNConnesse()} componenti connesse")
        )
        self._view.update_page()

    def handleGradoMax(self, e):
        self._view._txt_result.controls.clear()
        if not self._model.getNNodi():
            self._view._txt_result.controls.append(
                ft.Text(f"Creare prima il grafo!", color="red")
            )
            self._view.update_page()
            return
        nodo, grado=self._model.nodoMaxGrado()
        self._view._txt_result.controls.append(
            ft.Text(f"Nodo di grado max:\n"
                    f"{nodo}\n"
                    f"Grado: {grado}")
        )
        self._view.update_page()

    def handleDreamTeam(self, e):
        pass