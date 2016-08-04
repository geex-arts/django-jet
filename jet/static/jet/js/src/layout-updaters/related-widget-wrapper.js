var $ = require('jquery');

var RelatedWidgetWrapperUpdater = function() { };

RelatedWidgetWrapperUpdater.prototype = {
    replaceLinkIcon: function(selector) {
        var $img = $(selector);

        $('<span>')
            .addClass('related-widget-wrapper-icon')
            .insertAfter($img);
        $img.remove();
    },
    updateLinkIcons: function() {
        this.replaceLinkIcon(
            'img[src*="admin/img/icon-addlink"], img[src*="admin/img/icon_addlink"]'
        );
        this.replaceLinkIcon(
            'img[src*="admin/img/icon-changelink"]'
        );
        this.replaceLinkIcon(
            'img[src*="admin/img/icon-deletelink"]'
        );
        $('img[src*="admin/img/selector-search"]').remove();
        $('.add-related, .add-another, .change-related, .delete-related, .related-lookup').addClass('initialized');
    },
    updateLinks: function($select) {
        $select.find('~ .change-related, ~ .delete-related, ~ .add-another').each(function() {
            var $link = $(this);
            var hrefTemplate = $link.data('href-template');
            var value = $select.val();

            if (hrefTemplate == undefined) {
                return;
            }

            if (value) {
                $link.attr('href', hrefTemplate.replace('__fk__', value))
            } else {
                $link.removeAttr('href');
            }
        });
    },
    initLinks: function() {
        var obj = this;

        $('.form-row select').each(function() {
            var $select = $(this);

            obj.updateLinks($select);

            $select.find('~ .add-related, ~ .change-related, ~ .delete-related, ~ .add-another').each(function() {
                var $link = $(this);

                $link.on('click', function(e) {
                    e.preventDefault();

                    var href = $link.attr('href');

                    if (href != undefined) {
                        if (href.indexOf('_popup') == -1) {
                            href += (href.indexOf('?') == -1) ? '?_popup=1' : '&_popup=1';
                        }

                        obj.showPopup($select, href);
                    }
                });
            });
        }).on('change', function() {
            obj.updateLinks($(this));
        });

        $('.form-row input').each(function() {
            var $input = $(this);

            $input.find('~ .related-lookup').each(function() {
                var $link = $(this);

                $link.on('click', function(e) {
                    e.preventDefault();

                    var href = $link.attr('href');

                    href += (href.indexOf('?') == -1) ? '?_popup=1' : '&_popup=1';

                    obj.showPopup($input, href);
                });
            });
        });
    },
    initPopupBackButton: function() {
        var obj = this;

        $('.related-popup-back').on('click', function(e) {
            e.preventDefault();
            obj.closePopup();
        });
    },
    showPopup: function($input, href) {
        var $document = $(window.top.document);
        var $container = $document.find('.related-popup-container');
        var $loading = $container.find('.loading-indicator');
        var $body = $document.find('body').addClass('non-scrollable');
        var $popup = $('<iframe>')
            .attr('name', name)
            .attr('src', href)
            .data('input', $input)
            .addClass('related-popup')
            .on('load', function() {
                $popup.add($document.find('.related-popup-back')).fadeIn(200, 'swing', function() {
                    $loading.hide();
                });
            });

        $loading.show();
        $container.fadeIn(200, 'swing', function() {
            $container.append($popup);
        });
        $body.addClass('non-scrollable');
    },
    closePopup: function(response) {
        (function($) {
            var $document = $(window.top.document);
            var $popups = $document.find('.related-popup');
            var $container = $document.find('.related-popup-container');
            var $popup = $popups.last();

            if (response != undefined) {
                var $input = $popup.data('input');

                switch (response.action) {
                    case 'change':
                        $input.find('option').each(function() {
                            var $option = $(this);

                            if ($option.val() == response.value) {
                                $option.html(response.obj).val(response.new_value);
                            }
                        });

                        $input.trigger('change').trigger('select:init');

                        break;
                    case 'delete':
                        $input.find('option').each(function() {
                            var $option = $(this);

                            if ($option.val() == response.value) {
                                $option.remove();
                            }
                        });

                        $input.trigger('change').trigger('select:init');

                        break;
                    default:
                        if ($input.is('select')) {
                            var $option = $('<option>')
                                .val(response.value)
                                .html(response.obj);

                            $input.append($option);
                            $option.attr('selected', true);

                            $input
                                .trigger('change')
                                .trigger('select:init');
                        } else if ($input.is('input.vManyToManyRawIdAdminField') && $input.val()) {
                            $input.val($input.val() + ',' + response.value);
                        } else if ($input.is('input')) {
                            $input.val(response.value);
                        }

                        break;
                }
            }

            if ($popups.length == 1) {
                $container.fadeOut(200, 'swing', function() {
                    $document.find('.related-popup-back').hide();
                    $document.find('body').removeClass('non-scrollable');
                    $popup.remove();
                });
            } else {
                $popup.remove();
            }
        })(window.parent.jet.jQuery);
    },
    processPopupResponse: function() {
        var obj = this;

        $('#django-admin-popup-response-constants').each(function() {
            var $constants = $(this);
            var response = $constants.data('popup-response');

            obj.closePopup(response);
        });
    },
    overrideRelatedGlobals: function() {
        var obj = this;

        window.showRelatedObjectLookupPopup
            = window.showAddAnotherPopup
            = window.showRelatedObjectPopup
            = function() { };

        window.opener = window.parent;
        window.dismissRelatedLookupPopup = function(win, chosenId) {
            obj.closePopup({
                action: 'lookup',
                value: chosenId
            });
        };
    },
    initDeleteRelatedCancellation: function() {
        var obj = this;

        $('.popup.delete-confirmation .cancel-link').on('click', function(e) {
            e.preventDefault();
            obj.closePopup();
        }).removeAttr('onclick');
    },
    run: function() {
        try {
            this.updateLinkIcons();
            this.initLinks();
            this.initPopupBackButton();
            this.processPopupResponse();
            this.overrideRelatedGlobals();
            this.initDeleteRelatedCancellation();
            this.overrideRelatedGlobals();
        } catch (e) {
            console.error(e);
        }
    }
};

$(document).ready(function() {
    new RelatedWidgetWrapperUpdater().run();
});
