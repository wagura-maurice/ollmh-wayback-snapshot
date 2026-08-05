var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");
/**
 * @package     Expose
 * @version     4.0
 * @author      ThemeXpert http://www.themexpert.com
 * @copyright   Copyright (C) 2010 - 2011 ThemeXpert
 * @license     http://www.gnu.org/licenses/gpl-3.0.html GNU/GPLv3
 **/

(function (f) {

    f.fn.equalHeight = function (a) {
        var c = 0,
            b = [];
        this.each(function () {
            var c = a ? f(this).find(a) : f(this);
            b.push(c);
            //c.css("min-height", "")
        });

        //calculate max height
        this.each(function () {
            c = Math.max(c, f(this).outerHeight())
        });

        return this.each(function (a) {
            var total = b[a].length;
            if(total > 1) return;

            var a = b[a],
                g = f(this),
                g = a.height() + ( c - g.outerHeight() );

            a.css("min-height", g + "px")
        })
    };

})(jQuery);
}

/*
     FILE ARCHIVED ON 20:53:41 Mar 19, 2022 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 21:55:43 Aug 05, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 0.618
  load_resource: 83.997
  PetaboxLoader3.resolve: 55.896
  PetaboxLoader3.datanode: 27.401
*/