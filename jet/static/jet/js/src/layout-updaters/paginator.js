var $ = require('jquery');

var PaginatorUpdater = function($paginator) {
    this.$paginator = $paginator;
};

PaginatorUpdater.prototype = {
    removeSpacesBetweenPages: function() {
        this.$paginator.contents().each(function() {
            if (this.nodeType != 3) {
                return;
            }

            var $node = $(this);

            if (($node.prev().prop('tagName') == 'A' || $node.prev().prop('tagName') == 'SPAN')
                && ($node.next().prop('tagName') == 'A' || $node.next().prop('tagName') == 'SPAN')) {

                if ($.trim($node.text()) == '...') {
                    $node.wrap($('<span>').addClass('disabled'));
                } else {
                    $node.remove();
                }
            }
        });
    },
    wrapPages: function() {
        var foundPage = false;
        var pagesEnded = false;
        var $pageNodes = $([]);

        this.$paginator.contents().each(function() {
            var pageNode = this.tagName == 'A' || this.tagName == 'SPAN';

            if (pageNode) {
                foundPage = true;
            }

            if (!foundPage) {
                return;
            }

            if (pageNode && !pagesEnded) {
                var $node = $(this);

                $node.detach();
                $pageNodes = $pageNodes.add($node);
            } else {
                pagesEnded = true
            }
        });

        this.$paginator.prepend($('<span>').addClass('pages-wrapper').append($pageNodes));
    },
    wrapTextNodes: function() {
        var foundPage = false;
        var $nodes = $([]);

        this.$paginator.contents().each(function() {
            var pageNode = this.tagName == 'A' || this.tagName == 'SPAN';

            if (pageNode) {
                foundPage = true;
            } else if (foundPage && !pageNode && this.tagName != 'INPUT') {
                var $node = $(this);

                $node.detach();
                $nodes = $nodes.add($node);
            }
        });

        $('<div>')
            .addClass('label')
            .append($nodes)
            .appendTo(this.$paginator);
    },
    run: function() {
        try {
            this.removeSpacesBetweenPages();
            this.wrapPages();
            this.wrapTextNodes();
        } catch (e) {
            console.error(e, e.stack);
        }

        this.$paginator.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.paginator').each(function() {
        new PaginatorUpdater($(this)).run();
    });
});
