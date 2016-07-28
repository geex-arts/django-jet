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

                $node.remove();
                $pageNodes = $pageNodes.add($node);
            } else {
                pagesEnded = true
            }
        });

        this.$paginator.prepend($('<span>').addClass('pages-wrapper').append($pageNodes));
    },
    moveTextNodes: function() {
        var foundPage = false;
        var $nodes = $([]);

        this.$paginator.contents().each(function() {
            var pageNode = this.tagName == 'A' || this.tagName == 'SPAN';

            if (pageNode) {
                foundPage = true;
            } else if (foundPage && !pageNode && this.tagName != 'INPUT') {
                var $node = $(this);

                $node.remove();
                $nodes = $nodes.add($node);
            }
        });

        this.$paginator.prepend($nodes);
    },
    run: function() {
        try {
            this.removeSpacesBetweenPages();
            this.wrapPages();
            this.moveTextNodes();
        } catch (e) {
            console.error(e);
        }

        this.$paginator.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.paginator').each(function() {
        new PaginatorUpdater($(this)).run();
    });
});
