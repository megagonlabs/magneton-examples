from asyncio import sleep
from typing import Callable, Literal, Mapping
from ..core.widget.HistoryView import HistoryView
from ..core.widget.StateView import StateView
from ..core.widget.StatefulWidgetBase import StatefulWidgetBase
from ..core.widget import WidgetModel
from ..utils.mdump import mdump


class LinkedViews:
    def __init__(
        self,
        dataset,
        column_name,
        component_name="LinkedViews",
    ):
        # Initialize base widget
        base: StatefulWidgetBase = StatefulWidgetBase(component_name)

        # Initialize state
        base.state = {"data": {}}

        # Initialize transient state
        # Note: transient state is not saved in history
        base.model.t_state = {"is_loading": True}

        # Initialize actions
        self.init = base.define_action(self.init, recorded=True)
        self.select = base.define_action(self.select, recorded=True)
        
        # Initialize internals
        self.__base = base

        # Initialize data
        self.dataset = dataset
        self.column_name = column_name
        self.init()

    async def init(self):
        model = self.__base.model

        # Allow component to mount
        await sleep(0.1)

        # Fetch/update data
        data = {
                "distribution": self.get_distribution_by_column(),
                "index": -1,
                "table": self.get_data_table()
                }

        WidgetModel.unproxy(model.state.data).update(data)
        model.t_state.is_loading = False

    def get_data_table(self):
        df = self.dataset
        return list(df[self.column_name].unique())

    def get_distribution_by_column(self, column=None):
        result = []
        if column:
            df = self.dataset
            row = df[df[self.column_name] == column]
            dist = row.loc[:, row.columns != self.column_name].to_dict('records')[0]
            for key, value in dist.items():
                result.append({"x": key, "y": value})
        else:
            df = self.dataset.mean(axis=0, numeric_only=True)
            ls = self.dataset.columns
            for key in ls:
                if key != self.column_name:
                    result.append({"x": key, "y": df[key]})
        return result

    def select(self, element, component):
        model = self.__base.model

        # Set interaction state
        model.state.event_element = element
        model.state.event_component = component
        model.t_state.is_loading = True
        yield  # Allow component to render

        # Fetch/update data
        data = {
                "distribution": self.get_distribution_by_column(element),
                "index": self.get_data_table().index(element)
                }

        WidgetModel.unproxy(model.state.data).update(data)
        model.t_state.is_loading = False

    def debug(self, l=2):
        print(mdump(self.__base.model, l))

    def history(self):
        return HistoryView(self.__base)

    def get_state(self):
        return self.__base.state

    def view_state(self):
        return StateView(self.__base).show()

    def show(self):
        return self.__base.component()
