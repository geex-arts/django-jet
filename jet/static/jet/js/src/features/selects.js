require('select2');

var $ = require('jquery');
var t = require('../utils/translate');

var Select2 = function() { };

Select2.prototype = {
    updateAttachBody: function(AttachBody) {
        AttachBody.prototype._positionDropdown = function () {
            var $window = $(window);

            var isCurrentlyAbove = this.$dropdown.hasClass('select2-dropdown--above');
            var isCurrentlyBelow = this.$dropdown.hasClass('select2-dropdown--below');

            var newDirection = null;

            var position = this.$container.position();
            var offset = this.$container.offset();

            offset.bottom = offset.top + this.$container.outerHeight(false);

            var container = {
                height: this.$container.outerHeight(false)
            };

            container.top = offset.top;
            container.bottom = offset.top + container.height;

            var dropdown = {
                height: this.$dropdown.outerHeight(false)
            };

            var viewport = {
                top: $window.scrollTop(),
                bottom: $window.scrollTop() + $window.height()
            };

            var enoughRoomAbove = viewport.top < (offset.top - dropdown.height);
            var enoughRoomBelow = viewport.bottom > (offset.bottom + dropdown.height);

            var css = {
                left: offset.left,
                top: container.bottom
            };

            if (!isCurrentlyAbove && !isCurrentlyBelow) {
                newDirection = 'below';
            }

            if (!enoughRoomBelow && enoughRoomAbove && !isCurrentlyAbove) {
                newDirection = 'above';
            } else if (!enoughRoomAbove && enoughRoomBelow && isCurrentlyAbove) {
                newDirection = 'below';
            }

            if (newDirection == 'above' ||
                (isCurrentlyAbove && newDirection !== 'below')) {
                css.top = container.top - dropdown.height;
            }

            if (newDirection != null) {
                this.$dropdown
                    .removeClass('select2-dropdown--below select2-dropdown--above')
                    .addClass('select2-dropdown--' + newDirection);
                this.$container
                    .removeClass('select2-container--below select2-container--above')
                    .addClass('select2-container--' + newDirection);

                //hack
                var $search = this.$dropdown.find('.select2-search');

                if (newDirection == 'above' && $search.is(':first-child')) {
                    $search.detach().appendTo(this.$dropdown);
                } else if (newDirection == 'below' && $search.is(':last-child')) {
                    $search.detach().prependTo(this.$dropdown);
                }
            }

            this.$dropdownContainer.css(css);
        };

        AttachBody.prototype.render = function (decorated) {
            var $container = $('<span></span>');

            var $dropdown = decorated.call(this);
            $container.append($dropdown);

            this.$dropdownContainer = $container;

            //hack
            if (this.$element.prop('multiple')) {
                this.$dropdown.addClass('select2-multiple-dropdown');
            } else {
                this.$dropdown.removeClass('select2-multiple-dropdown');
            }

            return $container;
        };
    },
    updateDropdownAdapter: function(DropdownAdapter) {
        DropdownAdapter.prototype.render = function () {
            var buttons = '';

            if (this.options.get('multiple')) {
                buttons =
                    '<div class="select2-buttons">' +
                    '<a href="#" class="select2-buttons-button select2-buttons-button-select-all">' +
                    t('select all') +
                    '</a> ' +
                    '<a href="#" class="select2-buttons-button select2-buttons-button-deselect-all">' +
                    t('deselect all') +
                    '</a>' +
                    '</div>';
            }

            var $dropdown = $(
                '<span class="select2-dropdown">' +
                buttons +
                '<span class="select2-results"></span>' +
                '</span>'
            );

            var $element = this.$element;

            $dropdown.find('.select2-buttons-button-select-all').on('click', function (e) {
                e.preventDefault();
                var selected = [];
                $element.find('option').each(function () {
                    selected.push($(this).val());
                });
                $element.select2('val', selected);
                $element.select2('close');
            });

            $dropdown.find('.select2-buttons-button-deselect-all').on('click', function (e) {
                e.preventDefault();
                $element.select2('val', '');
                $element.select2('close');
            });

            $dropdown.attr('dir', this.options.get('dir'));
            this.$dropdown = $dropdown;
            return $dropdown;
        };
    },
    initSelect: function($select, DropdownAdapter) {
        var settings = {
            theme: 'jet',
            dropdownAdapter: DropdownAdapter,
            width: 'auto'
        };

        if ($select.hasClass('ajax')) {
            var contentTypeId = $select.data('content-type-id');
            var appLabel = $select.data('app-label');
            var model = $select.data('model');
            var objectId = $select.data('object-id');
            var pageSize = 100;

            settings['ajax'] = {
                dataType: 'json',
                data: function (params) {
                    return {
                        content_type: contentTypeId,
                        app_label: appLabel,
                        model: model,
                        q: params.term,
                        page: params.page,
                        page_size: pageSize,
                        object_id: objectId
                    };
                },
                processResults: function (data, params) {
                    if (data.error) {
                        return {}
                    }

                    params.page = params.page || 1;
                    var more = (params.page * pageSize) < data.total;

                    return {
                      results: data.items,
                      pagination: {
                        more: more
                      }
                    };
                }
            };
        }

        $select.on('change', function(e) {
            django.jQuery($select.get(0)).trigger(e);
        });

        $select.select2(settings);
    },
    initSelect2: function() {
        var self = this;
        var AttachBody = $.fn.select2.amd.require('select2/dropdown/attachBody');
        var DropdownAdapter = $.fn.select2.amd.require('select2/dropdown');
        var Utils = $.fn.select2.amd.require('select2/utils');
        var DropdownSearch = $.fn.select2.amd.require('select2/dropdown/search');
        var MinimumResultsForSearch = $.fn.select2.amd.require('select2/dropdown/minimumResultsForSearch');
        var closeOnSelect = $.fn.select2.amd.require('select2/dropdown/closeOnSelect');

        this.updateAttachBody(AttachBody);
        this.updateDropdownAdapter(DropdownAdapter);

        DropdownAdapter = Utils.Decorate(DropdownAdapter, DropdownSearch);
        DropdownAdapter = Utils.Decorate(DropdownAdapter, AttachBody);
        DropdownAdapter = Utils.Decorate(DropdownAdapter, MinimumResultsForSearch);
        DropdownAdapter = Utils.Decorate(DropdownAdapter, closeOnSelect);

        $(document).on('select:init', 'select', function() {
            var $select = $(this);

            if ($select.parents('.empty-form').length > 0) {
                return;
            }

            self.initSelect($select, DropdownAdapter);
        });

        $('select').trigger('select:init');

        $('.inline-group').on('inline-group-row:added', function(e, $inlineItem) {
            $inlineItem.find('select').trigger('select:init');
        });
    },
    run: function() {
        try {
            this.initSelect2();
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

$(document).ready(function() {
    new Select2().run();
});
