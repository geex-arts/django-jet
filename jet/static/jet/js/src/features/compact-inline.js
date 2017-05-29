var $ = require('jquery');

var CompactInline = function($inline) {
    this.$inline = $inline;
    this.prefix = $inline.data('inline-prefix');
    this.verboseName = $inline.data('inline-verbose-name');
    this.deleteText = $inline.data('inline-delete-text');
};

CompactInline.prototype = {
    updateLabels: function($inline) {
        var self = this;
        var $navigationItems = $inline.find('.inline-navigation-item');

        $inline.find('.inline-related').each(function(i) {
            var $inlineItem = $(this);
            var $label = $inlineItem.find('.inline_label');
            var label = $label.html().replace(/(#\d+)/g, "#" + (i + 1));
            var $navigationItem = $navigationItems.eq(i);
            var navigationLabel = $inlineItem.hasClass('has_original') ? label : self.verboseName + ' ' + label;

            $label.html(label);
            $navigationItem.html(navigationLabel);
        });
    },
    updateFormIndex: function($form, index) {
        var id_regex = new RegExp('(' + this.prefix + '-(\\d+|__prefix__))');
        var replacement = this.prefix + "-" + index;

        $form.find('*').each(function() {
            var $el = $(this);

            $.each(['for', 'id', 'name'], function() {
                var attr = this;

                if ($el.attr(attr)) {
                    $el.attr(attr, $el.attr(attr).replace(id_regex, replacement));
                }
            });
        });

        if (!$form.hasClass('empty-form')) {
            $form.attr('id', this.prefix + '-' + index);
        }
    },
    updateFormsIndexes: function($inline) {
        var self = this;
        var $navigationItems = $inline.find('.inline-navigation-item');

        $inline.find('.inline-related').each(function(i) {
            var $inlineItem = $(this);

            self.updateFormIndex($inlineItem, i);
            $navigationItems.eq(i).attr('data-inline-related-id', $inlineItem.attr('id'));
        });
    },
    updateTotalForms: function($inline) {
        var $totalFormsInput = $inline.find('[name="' + this.prefix + '-TOTAL_FORMS"]');
        var $maxFormsInput = $inline.find('[name="' + this.prefix + '-MAX_NUM_FORMS"]');
        var totalForms = parseInt($inline.find('.inline-related').length);
        var maxForms = $maxFormsInput.val() ? parseInt($maxFormsInput.val()) : Infinity;

        $totalFormsInput.val(totalForms);
        $inline.find('.add-row').toggle(maxForms >= totalForms);
    },
    addNavigationItem: function($inline, $inlineItem) {
        var $empty = $inline.find('.inline-navigation-item.empty');

        return $empty
            .clone()
            .removeClass('empty')
            .attr('data-inline-related-id', $inlineItem.attr('id'))
            .insertBefore($empty);
    },
    openNavigationItem: function($inline, $item) {
        $inline
            .find('.inline-related')
            .removeClass('selected')
            .filter('#' + $item.attr('data-inline-related-id'))
            .addClass('selected');

        $inline.find('.inline-navigation-item').removeClass('selected');
        $item.addClass('selected');
    },
    removeItem: function($inline, $item) {
        $item.remove();
        $inline.find('.inline-navigation-item[data-inline-related-id="' + $item.attr('id') + '"]').remove();
    },
    openFirstNavigationItem: function($inline) {
        var $item = $inline.find('.inline-navigation-item:not(.empty)').first();

        if ($item == undefined) {
            return;
        }

        this.openNavigationItem($inline, $item);
        this.scrollNavigationToTop($inline);
    },
    addItemDeleteButton: function($item) {
        $item
            .children(':first')
            .append('<span><a class="inline-deletelink" href="#">' + this.deleteText + "</a></span>");
    },
    scrollNavigationToTop: function($inline) {
        var $navigationItemsContainer = $inline.find('.inline-navigation-content');

        $navigationItemsContainer.stop().animate({
            scrollTop: 0
        });
    },
    scrollNavigationToBottom: function($inline) {
        var $navigationItemsContainer = $inline.find('.inline-navigation-content');

        $navigationItemsContainer.stop().animate({
            scrollTop: $navigationItemsContainer.prop('scrollHeight')
        });
    },
    initAdding: function($inline) {
        var self = this;

        $inline.find('.add-row a').on('click', function (e) {
            e.preventDefault();

            var $empty = $inline.find('.inline-related.empty-form');
            var cloneIndex = parseInt($inline.find('.inline-related').length) - 1;
            var $clone = $empty
                .clone(true)
                .removeClass('empty-form')
                .insertBefore($empty);

            self.updateTotalForms($inline);
            self.updateFormIndex($clone, cloneIndex);
            self.updateFormIndex($empty, cloneIndex + 1);

            var navigationItem = self.addNavigationItem($inline, $clone);

            self.updateLabels($inline);
            self.openNavigationItem($inline, navigationItem);
            self.addItemDeleteButton($clone);
            self.scrollNavigationToBottom($inline);
        });
    },
    initDeletion: function($inline) {
        var self = this;

        $inline.on('click', '.inline-deletelink', function(e) {
            e.preventDefault();

            var $inlineItem = $(this).closest('.inline-related');

            self.removeItem($inline, $inlineItem);
            self.updateFormsIndexes($inline);
            self.updateLabels($inline);
            self.updateTotalForms($inline);
            self.openFirstNavigationItem($inline);
        });

        $inline.find('.inline-related').each(function() {
            var $inlineItem = $(this);

            $inlineItem.find('.delete input').on('change', function() {
                $inline
                    .find('.inline-navigation-item[data-inline-related-id="' + $inlineItem.attr('id') + '"]')
                    .toggleClass('delete', $(this).is(':checked'));
            });
        });
    },
    initNavigation: function($inline) {
        var self = this;

        $inline.on('click', '.inline-navigation-item', function(e) {
            e.preventDefault();

            self.openNavigationItem($inline, $(this));
        });

        self.openFirstNavigationItem($inline);
    },
    run: function() {
        var $inline = this.$inline;

        try {
            this.initAdding($inline);
            this.initDeletion($inline);
            this.initNavigation($inline);
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

module.exports = CompactInline;
