var $ = require('jquery');
var t = require('../../utils/translate');

require('jquery-ui/ui/core');
require('jquery-ui/ui/widget');
require('jquery-ui/ui/mouse');
require('jquery-ui/ui/draggable');
require('jquery-ui/ui/resizable');
require('jquery-ui/ui/button');
require('jquery-ui/ui/dialog');

var SideBarBookmarks = function($sidebar) {
    this.$sidebar = $sidebar;
};

SideBarBookmarks.prototype = {
    addBookmark: function($form, $container) {
        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            dataType: 'json',
            data: $form.serialize(),
            success: function (result) {
                if (result.error) {
                    return;
                }

                var $item = $container
                    .find('.bookmark-item.clone')
                    .clone()
                    .removeClass('clone');

                $item
                    .attr('href', result.url)
                    .find('.sidebar-link-label')
                    .append(result.title);
                $item
                    .find('.bookmarks-remove')
                    .data('bookmark-id', result.id);

                $container.append($item);
            }
        });
    },
    deleteBookmark: function($form, $item) {
        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            dataType: 'json',
            data: $form.serialize(),
            success: function (result) {
                if (result.error) {
                    return;
                }

                $item.remove();
            }
        });
    },
    initBookmarksAdding: function($sidebar) {
        var self = this;
        var $form = $sidebar.find('#bookmarks-add-form');
        var $titleInput = $form.find('input[name="title"]');
        var $urlInput = $form.find('input[name="url"]');
        var $dialog = $sidebar.find('#bookmarks-add-dialog');
        var $container = $sidebar.find('.bookmarks-list');

        $sidebar.find('.bookmarks-add').on('click', function(e) {
            e.preventDefault();

            var $link = $(this);
            var defaultTitle = $link.data('title') ? $link.data('title') : document.title;
            var url = window.location.href;

            $titleInput.val(defaultTitle);
            $urlInput.val(url);

            var buttons = {};

            buttons[t('Add')] = function() {
                self.addBookmark($form, $container);
                $(this).dialog('close');
            };

            buttons[t('Cancel')] = function() {
                $(this).dialog('close');
            };

            $dialog.dialog({
                resizable: false,
                modal: true,
                buttons: buttons
            });
        });
    },
    initBookmarksRemoving: function($sidebar) {
        var self = this;
        var $form = $sidebar.find('#bookmarks-remove-form');
        var $idInput = $form.find('input[name="id"]');
        var $dialog = $sidebar.find('#bookmarks-remove-dialog');

        $sidebar.on('click', '.bookmarks-remove', function(e) {
            e.preventDefault();

            var $remove = $(this);
            var $item = $remove.closest('.bookmark-item');
            var bookmarkId = $remove.data('bookmark-id');

            $idInput.val(bookmarkId);

            var buttons = {};

            buttons[t('Delete')] = function() {
                self.deleteBookmark($form, $item);
                $(this).dialog('close');
            };

            buttons[t('Cancel')] = function() {
                $(this).dialog('close');
            };

            $dialog.dialog({
                resizable: false,
                modal: true,
                buttons: buttons
            });
        });
    },
    initBookmarks: function($sidebar) {
        this.initBookmarksAdding($sidebar);
        this.initBookmarksRemoving($sidebar);
    },
    run: function() {
        try {
            this.initBookmarksAdding(this.$sidebar);
            this.initBookmarksRemoving(this.$sidebar);
        } catch (e) {
            console.error(e, e.stack);
        }
    }
};

module.exports = SideBarBookmarks;
