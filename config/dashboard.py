import random
import json
from jet.dashboard.dashboard_modules.echarts import EchartsModule
from jet.dashboard.dashboard import Dashboard


class EchartsOptionsBuilder:
    def __init__(self):
        self.options = {
            'tooltip': {
                'trigger': 'axis',
                'axisPointer': {
                    'type': 'cross',
                    'label': {
                        'backgroundColor': '#6a7985'
                    }
                }
            },
            'toolbox': {
                'feature': {
                }
            },
            'xAxis': {
                'type': 'category',
                'boundaryGap': False,
                'data': []
            },
            'yAxis': {
                'type': 'value'
            },
            'series': []
        }

    def set_xaxis_list(self, xaxis_list):
        self.options['xAxis']['data'] = xaxis_list

    def set_series(self, series):
        self.options['series'] = series

    def set_style(self, basic_line=True, stack=False, show_area=False, show_legend=True, show_grid=True,
                  show_label=False, smooth=False
                  ):
        """

        :param basic_line: 默认样式Basic Line Charts <http://www.echartsjs.com/examples/editor.html?c=line-simple>
        :param stack : 堆积样式  <http://www.echartsjs.com/examples/editor.html?c=area-stack&theme=light>
        :param show_area : 显示阴影 <http://www.echartsjs.com/examples/editor.html?c=area-stack&theme=light>
        :param show_legend : 显示顶部分类
        :param show_grid
        :param show_label : 在点旁边显示数据
        :param smooth : 线是否平滑
        :return:
        """
        if basic_line:
            for record in self.options['series']:
                record['type'] = 'line'

        if stack:
            for record in self.options['series']:
                record['stack'] = "总量"

        if show_area:
            for record in self.options['series']:
                record['areaStyle'] = {}

        if show_legend:
            legends = [record['name'] for record in self.options['series']]
            self.options['legend'] = {
                'data': legends
            }

        if show_grid:
            self.options['grid'] = {
                'left': '3%',
                'right': '4%',
                'bottom': '3%',
                'containLabel': 'true'
            }

        if show_label:
            for record in self.options['series']:
                record['label'] = {
                    'normal': {
                        'show': 'true',
                        'position': 'top'
                    }
                }

        if smooth :
            for record in self.options['series']:
                record['smooth'] = True

    def add_tooltip(self):
        pass


class CustomIndexDashboard(Dashboard):
    columns = 2

    def load_visitor_source_options(self):
        series = [
            {
                'name': '邮件营销',
                'data': [random.randint(100, 300) for x in range(7)]
            },
            {
                'name': '联盟广告',
                'data': [random.randint(100, 300) for x in range(7)]
            },
            {
                'name': '视频广告',
                'data': [random.randint(100, 300) for x in range(7)]
            },
            {
                'name': '直接访问',
                'data': [random.randint(100, 300) for x in range(7)]
            },
            {
                'name': '搜索引擎',
                'data': [random.randint(100, 300) for x in range(7)]
            }
        ]
        xaxis_list = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        o = EchartsOptionsBuilder()
        o.set_series(series)
        o.set_xaxis_list(xaxis_list)
        o.set_style(
            stack=True,
            show_area=True,
            show_label=True,
            smooth=True
        )
        return json.dumps(o.options)

    def init_with_context(self, context):
        """

        :param context:
        :return:
        """

        self.children.append(EchartsModule(
            options=self.load_visitor_source_options()
        ))
