import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        # riferimenti ai dropdown, salvati quando vengono riempiti
        self._ddyear = None
        self._ddshape = None

    def fillDDYears(self, dd: ft.Dropdown):
        self._ddyear = dd
        years = self._model.getAllYears()
        for y in years:
            dd.options.append(ft.dropdown.Option(text=y))

    def fillDDShape(self, dd: ft.Dropdown):
        # salvo solo il riferimento: si popola dopo la selezione dell'anno
        self._ddshape = dd

    def handle_year_selected(self, e):
        year = self._ddyear.value
        if year is None:
            return
        # svuoto le shape della selezione precedente
        self._ddshape.options.clear()
        self._ddshape.value = None
        shapes = self._model.getAllShapes(year)
        for s in shapes:
            self._ddshape.options.append(ft.dropdown.Option(text=s))
        self._view.update_page()

    def handle_graph(self, e):
        year = self._ddyear.value
        shape = self._ddshape.value

        # validazione input
        if year is None:
            self._view.create_alert("Seleziona un anno")
            return
        if shape is None:
            self._view.create_alert("Seleziona una shape")
            return

        # creo il grafo
        self._model.creaGrafo(year, shape)
        nNodi, nArchi = self._model.getGraphDetails()

        # stampo i risultati nella ListView
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato per anno {year}, shape '{shape}'")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {nNodi}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {nArchi}")
        )

        somme = self._model.getSommaPesiAdiacenti()

        self._view.txt_result.controls.append(
            ft.Text("Somma dei pesi degli archi adiacenti per ogni stato:")
        )

        for stato, somma in somme:
            self._view.txt_result.controls.append(
                ft.Text(f"{stato}: {somma}")
            )

        self._view.update_page()


    def handle_path(self, e):
            pass