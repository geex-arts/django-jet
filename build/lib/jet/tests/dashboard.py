from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard


class TestIndexDashboard(Dashboard):
    columns = 3
    init_with_context_called = False

    class Media:
        js = ('file.js', 'file2.js')
        css = ('file.css', 'file2.css')

    def init_with_context(self, context):
        self.init_with_context_called = True
        self.available_children.append(modules.LinkList)
        self.available_children.append(modules.Feed)

        # append a recent actions module
        self.children.append(modules.RecentActions(
            'Recent Actions',
            10,
            column=0,
            order=1
        ))

        # append a feed module
        self.children.append(modules.Feed(
            'Latest Django News',
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5,
            column=1,
            order=1
        ))


class TestAppIndexDashboard(Dashboard):
    columns = 3
    init_with_context_called = False

    class Media:
        js = ('file.js', 'file2.js')
        css = ('file.css', 'file2.css')

    def init_with_context(self, context):
        self.init_with_context_called = True
        self.available_children.append(modules.LinkList)
        self.available_children.append(modules.Feed)

        # append a recent actions module
        self.children.append(modules.RecentActions(
            'Recent Actions',
            10,
            column=0,
            order=1
        ))

        # append a feed module
        self.children.append(modules.Feed(
            'Latest Django News',
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5,
            column=1,
            order=1
        ))
