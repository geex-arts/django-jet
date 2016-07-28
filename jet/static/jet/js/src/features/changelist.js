var $ = require('jquery');

var initChangelist = function() {
    var initChangelistHeaders = function() {
        var $originalThead = $('#changelist .results thead');

        if ($originalThead.length == 0) {
            return;
        }

        var $thead = $originalThead.clone();
        var $table = $('<table>').addClass('table helper').append($thead);

        $table.find('.action-checkbox-column').empty();
        $table.appendTo(document.body);

        var updateChangelistHeaderVisibility = function () {
            if ($(window).scrollTop() > $originalThead.offset().top) {
                $table.show();
            } else {
                $table.hide();
            }
        };

        var updateChangelistHeaderWidth = function () {
            var $originalTheadColumns = $originalThead.find('th');
            var $theadColumns = $thead.find('th');

            $originalTheadColumns.each(function (i) {
                $theadColumns.eq(i).css('width', $(this).width());
            });
        };

        $(window).on('scroll', updateChangelistHeaderVisibility);
        $(window).on('resize', updateChangelistHeaderWidth);

        updateChangelistHeaderWidth();
    };

    var initChangelistFooters = function() {
        var $changelistFooters = $('.changelist-footer');

        if ($changelistFooters.length == 0) {
            return;
        }

        var updateChangelistFooters = function () {
            $changelistFooters.each(function () {
                var $changelistFooter = $(this);
                var $results = $changelistFooter.siblings('.results');

                if ($results.length == 0) {
                    return;
                }

                if ($(window).scrollTop() + $(window).height() - $changelistFooter.outerHeight(false) < $results.offset().top + $results.outerHeight(false)) {
                    if (!$changelistFooter.hasClass('fixed')) {
                        var previousScrollTop = $(window).scrollTop();

                        $changelistFooter.addClass('fixed');
                        $results.css('margin-bottom', ($changelistFooter.outerHeight(false) - 20 - 2) + 'px');

                        $(window).scrollTop(previousScrollTop);
                    }
                } else {
                    if ($changelistFooter.hasClass('fixed')) {
                        $changelistFooter.removeClass('fixed');
                        $results.css('margin-bottom', 0);
                    }
                }
            });
        };

        $(window).on('scroll', updateChangelistFooters);
        $(window).on('resize', updateChangelistFooters);

        updateChangelistFooters();
    };

    var initChangelistImages = function() {
        $('img[src$="admin/img/icon-yes.gif"]').add('img[src$="admin/img/icon-yes.svg"]').after($('<span class="icon-tick">'));
        $('img[src$="admin/img/icon-no.gif"]').add('img[src$="admin/img/icon-no.svg"]').after($('<span class="icon-cross">'));
        $('img[src$="admin/img/icon-unknown.gif"]').add('img[src$="admin/img/icon-unknown.svg"]').after($('<span class="icon-question">'));
    };

    var initChangelistRowSelection = function() {
        $('#result_list tbody th, #result_list tbody td').on('click', function(e) {
            // Fix selection on clicking elements inside row (e.x. links)
            if (e.target != this) {
                return;
            }

            $(this).closest('tr').find('.action-checkbox .action-select').click();
        });
    };

    var initChangelistSortableSelection = function() {
        $('table thead .sortable').on('click', function(e) {

            if (e.target != this) {
                return;
            }

            var link = $(this).find('.text a').get(0);

            if (link != undefined) {
                link.click();
            }
        });
    };

    initChangelistHeaders();
    initChangelistFooters();
    initChangelistImages();
    initChangelistRowSelection();
    initChangelistSortableSelection();
};

$(document).ready(function() {
    initChangelist();
});
