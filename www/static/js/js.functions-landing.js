var screenWidth = $(window).width();
var screenHeight = $(window).height();

$(document).ready(function(){
	// Check if a new cache is available on page load. Swap it in and reload the page to get the new hotness.
	window.addEventListener('load', function(e) {
	  window.applicationCache.addEventListener('updateready', function(e) {
	    if (window.applicationCache.status == window.applicationCache.UPDATEREADY) {
	      // Browser downloaded a new app cache. Swap it in and reload the page to get the new hotness.
	      window.applicationCache.swapCache();
	      window.location.reload();
	    } 
	  }, false);
	}, false);	

	$(document).foundation(); 

    //force bookmark on iOS
    if (("standalone" in window.navigator) && !window.navigator.standalone && navigator.userAgent.match(/(iPod|iPhone)/i)){
        $('.landing-button-group, .landing-footer').hide();
        $('body').append('<div class="landing-footer-message">Tap "<b style="letter-spacing: -1px">Add to Home Screen</b>" to install</br><span>&#8595;</span></div>');
    } 
    if (("standalone" in window.navigator) && !window.navigator.standalone && navigator.userAgent.match(/(iPad)/i)){
        $('.landing-button-group, .landing-footer').hide();
        $('body').append('<div class="landing-footer-message ipad"><span>&#8593;</span></br>Tap <div class="safari-share-icon"></div> and then "<b style="letter-spacing: -1px">Add to Home Screen</b>" to install</div>');
    }
    if (navigator.userAgent.match(/(Android)/i)){
        $('body').append('<div class="landing-footer-message android"><span>&#8593;</span></br>Tap<div class="android-settings-icon"></div>and then "<b style="letter-spacing: -1px">Add to home screen</b>" to install</div>');
    }    
    //remove scroling: https://gist.github.com/amolk/1599412
    document.body.addEventListener('touchmove', function(event) {
      event.preventDefault();
    }, false);
    window.onresize = function() {
      $(document.body).width(window.innerWidth).height(window.innerHeight);
    }
    $(function() {
      window.onresize();
    });   

    //fastclick: https://github.com/ftlabs/fastclick
	window.addEventListener('load', function() {
	    FastClick.attach(document.body);
	}, false);
	$(function() {
	    FastClick.attach(document.body);
	});    

	//Define Click Event for Mobile
	if( 'ontouchstart' in window ){ var click = 'touchstart'; }
		else { var click = 'click'; }	

    $(".landing-container, .landing-container-wrapper").css('height', screenHeight);

	window.onload = function(){
	  $(".landing-container-wrapper, .landing-button").fadeIn(100);
	  $(".footer").fadeIn(300);
	};

	var heightDiv = $("#intro-info p").height();
	$('#intro-info').addClass('animated fadeInDownBig').css('top',screenHeight-heightDiv-220);
	$("#intro-info").css('height',heightDiv+210);	    

	$("#invite-code-button").on(click, function(){ 
		if ($("#invite-code-form").val() == "demoday"){
			$("#intro-info").fadeOut("slow");
		}
	});	

	$("#facebook-connect-btn").on(click, function(){ 
		window.location = '/auth/login/facebook';
	});    	

	$("#email-reg-btn").on(click, function(e){ 
		e.preventDefault();	
		$(".email-login-container").fadeIn(50);
		$("#facebook-connect-btn, #email-reg-btn").hide();
	});    

	$(".reset-passwd").on(click, function(e){ 
		e.preventDefault();	
		$(".email-login-container").hide();
		$(".email-reset-passwd-container").fadeIn(200);
	});	

	$("#back-login").on(click, function(e){ 
		e.preventDefault();	
		$(".email-login-container").hide();
		$("#facebook-connect-btn, #email-reg-btn").fadeIn(200);
	});

	$("#back-reset-passwd").on(click, function(e){ 
		e.preventDefault();	
		$(".email-reset-passwd-container").hide();
		$(".email-login-container").fadeIn(200);
	});	

	$("#terms").on(click, function(){ 
		alert("Terms");
	});

	$("#privacy").on(click, function(){ 
		alert("Privacy");
	});		
});
