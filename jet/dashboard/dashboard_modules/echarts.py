import random
import string
from jet.dashboard.modules import DashboardModule
from django.template.loader import render_to_string


class EchartsModule(DashboardModule):
    title = "Echarts"
    template = "jet.dashboard/modules/echarts.html"

    moduleid_list = []

    def __init__(self, options, module_id=None, *args, **kwargs):
        """

        :param module_id: 唯一标志符，每一个echarts组件在渲染的时候需要有一个唯一的DOM id
        :param args:
        :param kwargs:
        """

        if module_id in self.moduleid_list:
            raise RuntimeError("Your module_id must be unique to properly render echarts!")

        if not module_id:
            module_id = self.gene_moduleid()

        self.module_id = module_id
        self.options = options
        super(EchartsModule, self).__init__(*args, **kwargs)

    def set_options(self, options):
        self.options = options

    def gene_moduleid(self):
        module_id = "".join(random.choice(string.ascii_letters) for i in range(12))
        if not module_id in self.moduleid_list:
            return module_id
        return self.gene_moduleid()


class LineEchartsModule(EchartsModule):

    # 如果把options放在这里，就是所有实例共享的
    # 这不是我们想要的！

    def __init__(self, module_id, title=None, chart_title=None, save_as_image=False, show_tooltip=False,
                 show_legends=False, *args, **kwargs):

        """
        :param module_id : 唯一id
        :param title: 自定义标题
        :param chart_title : 图标的title
        :param save_as_image:
        :param show_tooltip
        :param show_lagends
        :param args:
        :param kwargs:
        """
        super(LineEchartsModule, self).__init__(*args, **kwargs)

        self.options = {
            'toolbox': {
                'feature': {
                }
            },
            'xAxis': {
                'type': 'category',
                'boundaryGap': 'false',
                'data': []
            },
            'yAxis': {
                'type': 'value'
            },
            'series': []
        }

        self.module_id = module_id

        if title:
            self.title = title

        if chart_title:
            self.options['title'] = {
                'text': chart_title
            }

        if show_tooltip:
            self.options['tooltip'] = {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'cross',
                    'label': {
                        'backgroundColor': '#6a7985'
                    }
                }
            }

        if show_legends:
            self.options['legend'] = {}

        if save_as_image:
            self.options['toolbox']['feature']["saveAsImage"] = {}

    def set_xAxis(self, xAxis_list):
        """

        :param xAxis_list: 横坐标
        :return:
        """

        self.options['xAxis']['data'] = xAxis_list

    def set_data_style(self, show_label=False, show_area=False, stack=False):
        """

        :param show_area: 如果为Ture，会显示曲线下方的阴影部分
        :param show_label: 是否在曲线旁边显示数据
        :param stack
        :return:
        """

        if len(self.options['series']) == 0:
            raise RuntimeError("you have not added data yet, please call add_data method first!")

        if show_area:
            for data in self.options['series']:
                data['areaStyle'] = {}

        if show_label:
            for data in self.options['series']:
                data['label'] = {
                    'normal': {
                        'show': 'true',
                        'position': 'top'
                    }
                }

        if stack:
            for data in self.options['series']:
                data['stack'] = "总量"

    def set_data(self, data):
        """

        :param name:
        :param data:
        :return:
        """

        if not data or not isinstance(data, list):
            raise RuntimeError("data parameter must be a none empty list!")

        self.options['series'] = data
