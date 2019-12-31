var $ = require('jquery');

var WindowStorage = function(name) {
    if (window.top[name] == undefined) {
        window.top[name] = [];
    }

    this.name = name;
};

WindowStorage.prototype = {
    push: function(window) {
        if (window.top[this.name][window.top[this.name].length - 1] == window) {
            return;
        }

        window.top[this.name].push(window);
    },
    pop: function() {
        window.top[this.name].pop();
    },
    previous: function() {
        if (window.top[this.name] == undefined
            || !$.isArray(window.top[this.name])
            || window.top[this.name].length < 2) {
            return null;
        }
        return window.top[this.name][window.top[this.name].length - 2];
    }
};

module.exports = WindowStorage;
