var screenWidth = $(window).width();
var screenHeight = $(window).height();

$(document).ready(function(){
//Common
	$(document).foundation(); 

    //force bookmark on iOS
    if (("standalone" in window.navigator) && !window.navigator.standalone && navigator.userAgent.match(/(iPod|iPhone|iPad)/)){
        $('.landing-button-group, .landing-footer').hide();
        $('body').append('<div class="landing-footer-message">Tap "<b style="letter-spacing: -1px">Add to Home Screen</b>" to install</br><span>&#8595;</span></div>');
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
	  backgroundChange();
	  $(".landing-container-wrapper, .landing-button").fadeIn(500);
	  $(".footer").fadeIn(100);
	  $(".app-name, .subheading").css("color","#fff");
	};

	//change background image
	var totalCount = 5;
	function backgroundChange() {
		var num = Math.ceil( Math.random() * totalCount );
		$(".landing-container").css('background','url(../static/img/landing-poster/'+num+'.png) no-repeat center center fixed').css('background-size','cover');
	}

	var heightDiv = $("#intro-info p").height();
	$('#intro-info').addClass('animated fadeInDownBig').css('top',screenHeight-heightDiv-220);
	$("#intro-info").css('height',heightDiv+210);	    

	$("#invite-code-button").on(click, function(){ 
		if ($("#invite-code-form").val() == "demoday"){
			$("#intro-info").fadeOut("slow");
		}
	});	

    /**
    * Handle redirect for Facebook login
    */
    $("#facebook-connect-btn").on(click, function(e){
        window.location.href = '/auth/login/facebook';
    });

	$("#email-reg-btn").on(click, function(){ 
		$(".email-login-container").fadeIn(50);
		$("#facebook-connect-btn, #email-reg-btn").hide();
	});    

	$(".reset-passwd").on(click, function(){ 
		$(".email-login-container").hide();
		$(".email-reset-passwd-container").fadeIn(200);
	});	

	$("#back-login").on(click, function(){ 
		$(".email-login-container").hide();
		$("#facebook-connect-btn, #email-reg-btn").fadeIn(200);
	});

	$("#back-reset-passwd").on(click, function(){ 
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
