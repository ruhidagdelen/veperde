/*

	Template Name: LIRA
    Template URI: https://devitems.com/html/lira-preview/
    Description: This is html5 template
    Author: BootExperts
    Author URI: https://devitems.com/
    Version: 1.0

*/
/*================================================
[  Table of contents  ]
================================================

	01. jQuery Mobile MeanMenu
	02. Home One Slide Owl Active
	03. Home Two Slide Owl Active
	04. Footer Gallery Owl Active
	05. Related Post Active
	06. Slide Post Active
	07. Home Three nivoSlider
	08. Home Four nivoSlider
	09. Mailchimp Active
	10. Masonary Section Active
	11. Magnific Popup For Image
	12. TOP Menu Stick
	13. scrollUp
	
================================================*/

(function ($) {
 "use strict";
 
	/*------ 01. jQuery Mobile MeanMenu ------*/
	jQuery('#mobile-nav').meanmenu();
	
	/*------ 02. Home One Slide Owl Active ------*/
   $('.active-home1').owlCarousel({
		loop:true,
		margin:0,
		nav:true,
		dots:false,
		autoplay: true,
		autoplaytimeout:2000,
		navText:["<i class='icofont icofont-long-arrow-left'></i>","<i class='icofont icofont-long-arrow-right'></i>"],
		responsive:{
			0:{
				items:1
			},
			600:{
				items:1
			},
			1000:{
				items:1
			}
		}
	})
	
	/*------ 03. Home Two Slide Owl Active ------*/
	$('.active-home2').owlCarousel({
		loop:true,
		margin:0,
		nav:false,
		dots:true,
		autoplay: true,
		autoplaytimeout:2000,
		navText:["<i class='icofont icofont-long-arrow-left'></i>","<i class='icofont icofont-long-arrow-right'></i>"],
		responsive:{
			0:{
				items:1
			},
			600:{
				items:1
			},
			1000:{
				items:1
			}
		}
	})
	
	/*------ 04. Footer Gallery Owl Active ------*/
	$('.footer-gallery').owlCarousel({
	  loop: true,
	  margin: 0,
	  autoplay: false,
	  nav: false,
	  dots:false,
	  responsive: {
		0: {
		  items: 2
		},
		600: {
		  items: 4
		},
		1000: {
		  items: 6
		}
	  }
	}) 
	
	/*------ 05. Related Post Active ------*/
	$('.related-post-cursol').owlCarousel({
	  loop: true,
	  margin: 0,
	  autoplay: false,
	  nav: false,
	  responsive: {
		0: {
		  items: 1
		},
		600: {
		  items: 2
		},
		1000: {
		  items: 2
		}
	  }
	}) 
	
	/*------ 06. Slide Post Active ------*/
	$('.slide-post-cursol').owlCarousel({
	  loop: true,
	  margin: 0,
	  autoplay: false,
	  nav: true,
	  dots:false,
	  navText:["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
	  responsive: {
		0: {
		  items: 1
		},
		600: {
		  items: 1
		},
		1000: {
		  items: 1
		}
	  }
	}) 
	
	/*------ 07. Home Three nivoSlider ------*/  
	$('#slider').nivoSlider({
        effect: 'random',
        slices: 25,
        boxCols: 10,
        boxRows: 8,
        animSpeed: '600',
        pauseTime: '4000',
        startSlide: 0,
        directionNav: false,
        controlNav: 0,
        controlNavThumbs: false,
        pauseOnHover: false,
        manualAdvance: false,
        prevText: '<i class="fa fa-angle-left nivo-prev-icon"></i>',
        nextText: '<i class="fa fa-angle-right nivo-next-icon"></i>'
    });
	
	/*------ 08. Home Four nivoSlider ------*/  
	$('#slider-hm-4').nivoSlider({
        effect: 'random',
        slices: 25,
        boxCols: 10,
        boxRows: 8,
        animSpeed: '600',
        pauseTime: '4000',
        startSlide: 0,
        directionNav: true,
        controlNav: 0,
        controlNavThumbs: false,
        pauseOnHover: false,
        manualAdvance: false,
        prevText: '<i class="icofont icofont-long-arrow-left"></i>',
        nextText: '<i class="icofont icofont-long-arrow-right"></i>'
    });
	
	/*------ 09. Mailchimp Active ------*/
	$('#mc-form').ajaxChimp({
		 language: 'en',
		 callback: mailChimpResponse,
		 // ADD YOUR MAILCHIMP URL BELOW HERE!
		 url: 'http://themeshaven.us8.list-manage.com/subscribe/post?u=759ce8a8f4f1037e021ba2922&amp;id=a2452237f8'
		});
		function mailChimpResponse(resp) {
		 
		 if (resp.result === 'success') {
		  $('.mailchimp-success').html('' + resp.msg).fadeIn(900);
		  $('.mailchimp-error').fadeOut(400);
		  
		 } else if(resp.result === 'error') {
		  $('.mailchimp-error').html('' + resp.msg).fadeIn(900);
		 }  
		}
		
	/*------ 10. Masonary Section Active ------*/
	$('.grid').imagesLoaded( function() {
		
		// init Isotope
		var $grid = $('.grid').isotope({
		  itemSelector: '.grid-item',
		  percentPosition: true,
		  masonry: {
			// use outer width of grid-sizer for columnWidth
			columnWidth: '.grid-item',
		  }
		});	

	});		
	
	/*------ 11. Magnific Popup For Image ------*/
	$('.venobox').magnificPopup({
	  type: 'image',
	  gallery: {
			  enabled: true, // set to true to enable gallery
			}
	});
	
	/*------ 12. TOP Menu Stick ------*/
	// $(window).on('scroll',function() {
	//    var scroll = $(window).scrollTop();
	//    if (scroll < 245) {
	// 	$("#sticky-header").removeClass("sticky");
	//    }else{
	// 	$("#sticky-header").addClass("sticky");
	//    }
	// });
	
	/*------ 13. scrollUp ------*/
	$.scrollUp({
		scrollText: '<i class="fa fa-angle-up"></i>',
		easingType: 'linear',
		scrollSpeed: 900,
		animation: 'fade'
	});
	
})(jQuery);  