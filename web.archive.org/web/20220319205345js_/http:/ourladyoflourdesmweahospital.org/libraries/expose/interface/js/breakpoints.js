var _____WB$wombat$assign$function_____=function(name){return (globalThis._wb_wombat && globalThis._wb_wombat.local_init && globalThis._wb_wombat.local_init(name))||globalThis[name];};if(!globalThis.__WB_pmw){globalThis.__WB_pmw=function(obj){this.__WB_source=obj;return this;}}{
let window = _____WB$wombat$assign$function_____("window");
let self = _____WB$wombat$assign$function_____("self");
let document = _____WB$wombat$assign$function_____("document");
let location = _____WB$wombat$assign$function_____("location");
let top = _____WB$wombat$assign$function_____("top");
let parent = _____WB$wombat$assign$function_____("parent");
let frames = _____WB$wombat$assign$function_____("frames");
let opener = _____WB$wombat$assign$function_____("opener");
/*
	Breakpoints.js
	version 1.0
	
	Creates handy events for your responsive design breakpoints
	
	Copyright 2011 XOXCO, Inc
	http://xoxco.com/

	Documentation for this plugin lives here:
	http://xoxco.com/projects/code/breakpoints
	
	Licensed under the MIT license:
	http://www.opensource.org/licenses/mit-license.php

*/(function(e){var t=0,n=null;e.fn.resetBreakpoints=function(){e(window).unbind("resize");n&&clearInterval(n);t=0};e.fn.setBreakpoints=function(r){var i=jQuery.extend({distinct:!0,breakpoints:new Array(320,480,768,1024)},r);n=setInterval(function(){var n=e(window).width(),r=!1;for(var s in i.breakpoints.sort(function(e,t){return t-e})){if(!r&&n>=i.breakpoints[s]&&t<i.breakpoints[s]){if(i.distinct){for(var o in i.breakpoints.sort(function(e,t){return t-e}))if(e("body").hasClass("breakpoint-"+i.breakpoints[o])){e("body").removeClass("breakpoint-"+i.breakpoints[o]);e(window).trigger("exitBreakpoint"+i.breakpoints[o])}r=!0}e("body").addClass("breakpoint-"+i.breakpoints[s]);e(window).trigger("enterBreakpoint"+i.breakpoints[s])}if(n<i.breakpoints[s]&&t>=i.breakpoints[s]){e("body").removeClass("breakpoint-"+i.breakpoints[s]);e(window).trigger("exitBreakpoint"+i.breakpoints[s])}if(i.distinct&&n>=i.breakpoints[s]&&n<i.breakpoints[s-1]&&t>n&&t>0&&!e("body").hasClass("breakpoint-"+i.breakpoints[s])){e("body").addClass("breakpoint-"+i.breakpoints[s]);e(window).trigger("enterBreakpoint"+i.breakpoints[s])}}t!=n&&(t=n)},250)}})(jQuery);
}

/*
     FILE ARCHIVED ON 21:02:54 Jan 28, 2022 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 21:55:44 Aug 05, 2026.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  capture_cache.get: 0.476
  load_resource: 25.44
  PetaboxLoader3.datanode: 24.712
*/