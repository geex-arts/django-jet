try:
    from django.core.management.base import NoArgsCommand
except ImportError:
    from django.core.management import BaseCommand as NoArgsCommand

from jet.utils import get_app_list


class Command(NoArgsCommand):
    help = 'Generates example of JET custom apps setting'
    item_order = 0
    
    def handle(self, *args, **options):
        if args:
            raise CommandError("Command doesn't accept any arguments")
        return self.handle_noargs(**options)
    
    def handle_noargs(self, **options):
        class User:
            is_active = True
            is_staff = True
            is_superuser = True

            def has_module_perms(self, app):
                return True

            def has_perm(self, object):
                return True

        class Request:
            user = User()

        app_list = get_app_list({
            'request': Request(),
            'user': None
        })

        self.stdout.write('# Add this to your settings.py to customize applications and models list')
        self.stdout.write('JET_SIDE_MENU_CUSTOM_APPS = [')

        for app in app_list:
            app_label = app.get('app_label', app.get('name'))

            self.stdout.write('    (\'%s\', [' % app_label)
            for model in app['models']:
                self.stdout.write('        \'%s\',' % model['object_name'])
            self.stdout.write('    ]),')

        self.stdout.write(']')
