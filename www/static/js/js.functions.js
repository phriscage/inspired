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
	//Define Click Event for Mobile
	if( 'ontouchstart' in window ){ 
		var click = 'singleTap'; 
	}else{ 
		var click = 'click';
	}	

    $("#spinner").css('top', screenHeight/2+10);

	window.onload = function(){
	  $(".spinner-wrap").fadeOut(50);
	  $(".footer").fadeIn(100);
	};  	

/*FOOTER BUTTONS*/
  //Settings MENU
	/*	Reveal Menu */
	$('.footer-settings').on(click, function(e){
		e.stopImmediatePropagation();
		e.preventDefault();	
		if( !$('.content').hasClass('inactive') ){				
			// Slide and scale content		
			$('.footer').hide();
			$('.content, .settings-menu').addClass('inactive');
			setTimeout(function(){ $('.content').addClass('flag'); }, 100);
			
			// Change status bar
			$('.status').fadeOut(100, function(){
				$(this).toggleClass('active').fadeIn(300);
			});
			
			// Slide in menu links
			var timer = 0;
			$.each($('li'), function(i,v){
				timer = 40 * i;
				setTimeout(function(){
					$(v).addClass('visible');
				}, timer);
			});
		}
	});

	/*	Close Menu */
	function closeMenu() {		
		// Slide and scale content
		$('.content, .settings-menu').removeClass('inactive flag');
		
		// Change status bar
		$('.status').fadeOut(100, function(){
			$(this).toggleClass('active').fadeIn(300);
		});

		// $(".fx-container").css("width", screenWidth);			
		
		// Reset menu
		setTimeout(function(){
			$('li').removeClass('visible');
			$('.footer').fadeIn(100);
		}, 300);
	}
	
	$('.content').on(click, function(){
		if( $('.content').hasClass('flag') ){
			closeMenu();
		}
	});
	$('.settings-back').on(click, function(e){
		e.preventDefault();
		closeMenu();
	});
	$('.settings-back-back').on(click, function(){
		$('.settings-back-back').hide();
		$('.settings-menu-list, .settings-back').show();
		$(".ajax-container").html("");
		$('.settings-title').text('Settings');
	});	
	$('.my-profile').on(click,function(){
	   $.ajax({
	      url:"/static/templates/settings/my-profile.html",
	      dataType:'html',
	      success:function(data) {
	        $(".ajax-container").html(data);
	      }
	   });
	   $('.settings-title').text('My Profile');
	   $('.settings-footer, .settings-menu-list, .settings-back').hide();
	   $('.settings-back-back').show();
	});	
	$('.email-preferences').on(click,function(){
	   $.ajax({
	      url:"/static/templates/settings/email-preferences.html",
	      dataType:'html',
	      success:function(data) {
	        $(".ajax-container").html(data);
	      }
	   });
	   $('.settings-title').text('Email Preferences');
	   $('.settings-footer, .settings-menu-list, .settings-back').hide();
	   $('.settings-back-back').show();
	});		
	$('.invite-friends').on(click,function(){
	   $.ajax({
	      url:"../templates/settings/invite-friends.html",
	      dataType:'html',
	      success:function(data) {
	        $(".ajax-container").html(data);
	      }
	   });
	   $('.settings-title').text('Invite Friends');
	   $('.settings-footer, .settings-menu-list, .settings-back').hide();
	   $('.settings-back-back').show();
	});
	$('.send-feedback').on(click,function(){
	   $.ajax({
	      url:"../templates/settings/send-feedback.html",
	      dataType:'html',
	      success:function(data) {
	        $(".ajax-container").html(data);
	      }
	   });
	   $('.settings-title').text('Send Feedback');
	   $('.settings-footer, .settings-menu-list, .settings-back').hide();
	   $('.settings-back-back').show();
	});	
	$('.help').on(click,function(){
	   $.ajax({
	      url:"../templates/settings/help.html",
	      dataType:'html',
	      success:function(data) {
	        $(".ajax-container").html(data);
	      }
	   });
	   $('.settings-title').text('Help');
	   $('.settings-footer, .settings-menu-list, .settings-back').hide();
	   $('.settings-back-back').show();
	});	
	$('.legal').on(click,function(){
	   $.ajax({
	      url:"../templates/settings/legal.html",
	      dataType:'html',
	      success:function(data) {
	        $(".ajax-container").html(data);
	      }
	   });
	   $('.settings-title').text('Legal');
	   $('.settings-footer, .settings-menu-list, .settings-back').hide();
	   $('.settings-back-back').show();
	});
  //END Settings MENU
  //Bookmark & Following buttons
    $('a.footer-btn').on(click, function(e){
        e.preventDefault();
        var position = $('#footer-container').position();
        if ($(this).hasClass('footer-bookmarks')){
        	var divActive = 'bookmarks';
        	var divInactive = 'following';
        } else {
        	var divActive = 'following';
        	var divInactive = 'bookmarks';
        }
        if ($('.footer-'+divInactive).hasClass('selected')){
        	$("#footer-container").html('');
			$.ajax({
				url:"../templates/footer/"+divActive+".html",
				dataType:'html',
				success:function(data) {
					$("#footer-container").html(data);
				}
			});	
			$(this).addClass('selected');
			$('.footer-'+divInactive).removeClass('selected');
        }else{
	        if(position.top == 1200){
	        	$(this).addClass('selected');
	        	$(".main-container").css('height',screenHeight);
	        	$("#footer-container").css('height',screenHeight-88);
				$.ajax({
					url:"../templates/footer/"+divActive+".html",
					dataType:'html',
					success:function(data) {
						$("#footer-container").html(data);
					}
				});	
				$('#footer-container').attr('class', '').addClass('move-up');
	        }else{
	        	$(".main-container").css('height','100%');
	            $('#footer-container').attr('class', '').addClass('move-down');
	            $(this).removeClass('selected');
	        }
    	}
    });
    $("#footer-container").bind("oanimationend animationend webkitAnimationEnd", function(){
        if($("#footer-container").hasClass('move-up')) $("#footer-container").addClass('move-up-final');
        if($("#footer-container").hasClass('move-down')) $("#footer-container").addClass('move-down-final');
    });   

//Artist Screen
	$(".follow-btn").on(click,function(){
	  $(this).toggleClass('selected');
	});

//Video Screen
	$(".video-poster iframe").css({
		width: screenWidth,
		height: screenWidth/1.333333333333
	});

//Product Screen
	$("#bookmark-item-btn").on(click,function(e){
		e.preventDefault();			
	  $(this).toggleClass('selected');
	});

    $(".maximize-btn").on(click, function(e){ 
		e.stopImmediatePropagation();
    	$(".clearing-featured-img img").click(); 
    }); 

//Retailer Button
    $(".retailer-btn").on(click, function(){ 
	    var retailerUrl = $(".retailer-btn").attr("data-src");

		if( 'ontouchstart' in window ){//touch device
			var win=window.open(retailerUrl, '_blank');
			win.focus();
		}else{//non-touch device
			$("#footer-container-iframe").attr("src",retailerUrl); 

	    	$(".main-container").css('height',screenHeight);
	    	$("#footer-container-iframe").css('height',screenHeight-88);
	    	$("#footer-container-iframe").attr("seamless","yes");        	
			$("#footer-container").css('overflow-y','hidden');    		
	    	$("#footer-container").css('padding-left','0');
	    	
	    	$(".back-btn").hide();

			$(".footer-btn, .footer-settings").fadeOut();
			$(".footer-retailer-back, .footer-retailer-fwd").fadeIn();    		
	    	$(".close-retailer-btn").show();
	    	var retailerName = retailerUrl.replace("http://go.redirectingat.com?id=35687X941090&xs=1&url=http%3A%2F%2F","").replace("http://", "").replace("https://", "").split(/([\%\/])/);
	    	$(".name").text(retailerName[0]).css("font-size","18px").attr('onclick', '');
	    	
			$('#footer-container').attr('class', '').addClass('move-up');
			//define variable to store iframe history state
			window.historyState = history.length;
			window.originalHistoryState = history.length;
			$(".footer-retailer-fwd").addClass('inactive');			
		}
    });

	$(".footer-retailer-back").on(click, function(e){ 
		e.preventDefault();
		if ($(".footer-retailer-fwd").hasClass('inactive')){
			window.historyState = history.length;
		}
		if (window.originalHistoryState == window.historyState){
			 $("a.close-retailer-btn").trigger(click);
		}else{
			window.historyState--;
			$(".footer-retailer-fwd").removeClass('inactive');
			history.back();
		}
	});

	$(".footer-retailer-fwd").on(click, function(e){ 
		e.preventDefault();
		if (history.length == window.historyState){
			$(this).addClass('inactive');
		}else{
			window.historyState++;
			if (history.length == window.historyState){
				$(this).addClass('inactive');
			}
			history.forward();			
		}
	});	

    $(".close-retailer-btn").on(click, function(e){
		e.stopImmediatePropagation();
		e.preventDefault();	
    	$(".main-container").css('height','100%');
    	$(".back-btn, .footer-btn, .footer-settings").fadeIn();
    	$(".footer").css('bottom','0');
    	$(".close-retailer-btn, .footer-retailer-back, .footer-retailer-fwd").hide();
    	$(".name").text("Inspired").css("font-size","32px").fadeIn();
    	$(".name").attr("onclick", "location.reload();location.href='../../../music.html'");  
    	$("#footer-container").css('overflow-y','scroll');    		  	
        $('#footer-container').attr('class', '').addClass('move-down');
        $("#footer-container-iframe").attr('src','');
        $(this).removeClass('selected');
    });   
});
