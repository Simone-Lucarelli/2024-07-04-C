import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value
        if (year is not None and shape is not None):
            self._model.build_graph(year, shape)
            res1 = self._model.print_graph()
            res2 = self._model.max_edges()
            self._view.txt_result1.controls.append(ft.Text(res1))
            self._view.txt_result1.controls.append(ft.Text(res2))
            self._view.update_page()
        else:
            self._view.create_alert("Inserire anno e forma prima di creare il grafo")


    def handle_path(self, e):
        max_weight, path = self._model.find_path()
        print(max_weight, path)

    def fill_dd_years(self):
        years = self._model.get_years()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()
        print(f"Called fill_dd_year. Years: {years}")

    def fill_dd_shape(self, e):
        year = self._view.ddyear.value
        shapes = self._model.get_shapes(year)
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()
        print("Called fill_dd_shape for year " + year)
