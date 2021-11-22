/*
    A simple jQuery jmodal (http://github.com/kylefox/jquery-jmodal)
    Version 0.9.1
*/

(function (factory) {
  // Making your jQuery plugin work better with npm tools
  // http://blog.npmjs.org/post/112712169830/making-your-jquery-plugin-work-better-with-npm
  if(typeof module === "object" && typeof module.exports === "object") {
    factory(require("jquery"), window, document);
  }
  else {
    factory(jQuery, window, document);
  }
}(function($, window, document, undefined) {

  var jmodals = [],
      getCurrent = function() {
        return jmodals.length ? jmodals[jmodals.length - 1] : null;
      },
      selectCurrent = function() {
        var i,
            selected = false;
        for (i=jmodals.length-1; i>=0; i--) {
          if (jmodals[i].$blocker) {
            jmodals[i].$blocker.toggleClass('current',!selected).toggleClass('behind',selected);
            selected = true;
          }
        }
      };

  $.jmodal = function(el, options) {
    var remove, target;
    this.$body = $('body');
    this.options = $.extend({}, $.jmodal.defaults, options);
    this.options.doFade = !isNaN(parseInt(this.options.fadeDuration, 10));
    this.$blocker = null;
    if (this.options.closeExisting)
      while ($.jmodal.isActive())
        $.jmodal.close(); // Close any open jmodals.
    jmodals.push(this);
    if (el.is('a')) {
      target = el.attr('href');
      this.anchor = el;
      //Select element by id from href
      if (/^#/.test(target)) {
        this.$elm = $(target);
        if (this.$elm.length !== 1) return null;
        this.$body.append(this.$elm);
        this.open();
      //AJAX
      } else {
        this.$elm = $('<div>');
        this.$body.append(this.$elm);
        remove = function(event, jmodal) { jmodal.elm.remove(); };
        this.showSpinner();
        el.trigger($.jmodal.AJAX_SEND);
        $.get(target).done(function(html) {
          if (!$.jmodal.isActive()) return;
          el.trigger($.jmodal.AJAX_SUCCESS);
          var current = getCurrent();
          current.$elm.empty().append(html).on($.jmodal.CLOSE, remove);
          current.hideSpinner();
          current.open();
          el.trigger($.jmodal.AJAX_COMPLETE);
        }).fail(function() {
          el.trigger($.jmodal.AJAX_FAIL);
          var current = getCurrent();
          current.hideSpinner();
          jmodals.pop(); // remove expected jmodal from the list
          el.trigger($.jmodal.AJAX_COMPLETE);
        });
      }
    } else {
      this.$elm = el;
      this.anchor = el;
      this.$body.append(this.$elm);
     // this.open();
    }
  };

  $.jmodal.prototype = {
    constructor: $.jmodal,

    open: function() {
      var m = this;
      this.block();
      this.anchor.blur();
      if(this.options.doFade) {
        setTimeout(function() {
          m.show();
        }, this.options.fadeDuration * this.options.fadeDelay);
      } else {
        this.show();
      }
      $(document).off('keydown.jmodal').on('keydown.jmodal', function(event) {
        var current = getCurrent();
        if (event.which === 27 && current.options.escapeClose) current.close();
      });
      if (this.options.clickClose)
        this.$blocker.click(function(e) {
          if (e.target === this)
            $.jmodal.close();
        });
    },

    close: function() {
      jmodals.pop();
      this.unblock();
      this.hide();
      if (!$.jmodal.isActive())
        $(document).off('keydown.jmodal');
    },

    block: function() {
      this.$elm.trigger($.jmodal.BEFORE_BLOCK, [this._ctx()]);
      this.$body.css('overflow','hidden');
      this.$blocker = $('<div class="' + this.options.blockerClass + ' blocker current"></div>').appendTo(this.$body);
      selectCurrent();
      if(this.options.doFade) {
        this.$blocker.css('opacity',0).animate({opacity: 1}, this.options.fadeDuration);
      }
      this.$elm.trigger($.jmodal.BLOCK, [this._ctx()]);
    },

    unblock: function(now) {
      if (!now && this.options.doFade)
        this.$blocker.fadeOut(this.options.fadeDuration, this.unblock.bind(this,true));
      else {
        this.$blocker.children().appendTo(this.$body);
        this.$blocker.remove();
        this.$blocker = null;
        selectCurrent();
        if (!$.jmodal.isActive())
          this.$body.css('overflow','');
      }
    },

    show: function() {
      this.$elm.trigger($.jmodal.BEFORE_OPEN, [this._ctx()]);
      if (this.options.showClose===true) {
        this.closeButton = $('<a href="#close-jmodal" rel="jmodal:close" class="close-jmodal ' + this.options.closeClass + '">' + this.options.closeText + '</a>');
        this.$elm.append(this.closeButton);
      }
      this.$elm.addClass(this.options.jmodalClass).appendTo(this.$blocker);
      if(this.options.doFade) {
        this.$elm.css({opacity: 0, display: 'inline-block'}).animate({opacity: 1}, this.options.fadeDuration);
      } else {
        this.$elm.css('display', 'inline-block');
      }
      this.$elm.trigger($.jmodal.OPEN, [this._ctx()]);
    },

    hide: function() {
      this.$elm.trigger($.jmodal.BEFORE_CLOSE, [this._ctx()]);
      if (this.closeButton) this.closeButton.remove();
      var _this = this;
      if(this.options.doFade) {
        this.$elm.fadeOut(this.options.fadeDuration, function () {
          _this.$elm.trigger($.jmodal.AFTER_CLOSE, [_this._ctx()]);
        });
      } else {
        this.$elm.hide(0, function () {
          _this.$elm.trigger($.jmodal.AFTER_CLOSE, [_this._ctx()]);
        });
      }
      this.$elm.trigger($.jmodal.CLOSE, [this._ctx()]);
    },

    showSpinner: function() {
      if (!this.options.showSpinner) return;
      this.spinner = this.spinner || $('<div class="' + this.options.jmodalClass + '-spinner"></div>')
        .append(this.options.spinnerHtml);
      this.$body.append(this.spinner);
      this.spinner.show();
    },

    hideSpinner: function() {
      if (this.spinner) this.spinner.remove();
    },

    //Return context for custom events
    _ctx: function() {
      return { elm: this.$elm, $elm: this.$elm, $blocker: this.$blocker, options: this.options };
    }
  };

  $.jmodal.close = function(event) {
    if (!$.jmodal.isActive()) return;
    if (event) event.preventDefault();
    var current = getCurrent();
    current.close();
    return current.$elm;
  };

  // Returns if there currently is an active jmodal
  $.jmodal.isActive = function () {
    return jmodals.length > 0;
  };

  $.jmodal.getCurrent = getCurrent;

  $.jmodal.defaults = {
    closeExisting: true,
    escapeClose: true,
    clickClose: true,
    closeText: 'Close',
    closeClass: '',
    jmodalClass: "jmodal",
    blockerClass: "jquery-jmodal",
    spinnerHtml: '<div class="rect1"></div><div class="rect2"></div><div class="rect3"></div><div class="rect4"></div>',
    showSpinner: true,
    showClose:true,
    fadeDuration:200,   // Number of milliseconds the fade animation takes.
    fadeDelay:0.6        // Point during the overlay's fade-in that the jmodal begins to fade in (.5 = 50%, 1.5 = 150%, etc.)
  };

  // Event constants
  $.jmodal.BEFORE_BLOCK = 'jmodal:before-block';
  $.jmodal.BLOCK = 'jmodal:block';
  $.jmodal.BEFORE_OPEN = 'jmodal:before-open';
  $.jmodal.OPEN = 'jmodal:open';
  $.jmodal.BEFORE_CLOSE = 'jmodal:before-close';
  $.jmodal.CLOSE = 'jmodal:close';
  $.jmodal.AFTER_CLOSE = 'jmodal:after-close';
  $.jmodal.AJAX_SEND = 'jmodal:ajax:send';
  $.jmodal.AJAX_SUCCESS = 'jmodal:ajax:success';
  $.jmodal.AJAX_FAIL = 'jmodal:ajax:fail';
  $.jmodal.AJAX_COMPLETE = 'jmodal:ajax:complete';

  $.fn.jmodal = function(options){
    if (this.length === 1) {
      new $.jmodal(this, options);
    }
    return this;
  };

  // Automatically bind links with rel="jmodal:close" to, well, close the jmodal.
  $(document).on('click.jmodal', 'a[rel~="jmodal:close"]', $.jmodal.close);
  $(document).on('click.jmodal', 'a[rel~="jmodal:open"]', function(event) {
    event.preventDefault();
    $(this).jmodal();
  });
}));
