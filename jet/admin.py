from django.contrib import admin


class CompactInline(admin.options.InlineModelAdmin):
    template = 'admin/edit_inline/compact.html'
