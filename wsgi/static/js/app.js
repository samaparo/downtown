/*global $ */
/*global console */
var imageTemplate;
var currentPage = 0;
(function () {
	'use strict';
	currentPage = 0;
	imageTemplate = $("#template_image").html();
	
	$("#buttonWrapper button").click(function () {
		var $button = $(this);
		var $loading = $("#buttonWrapper #loading");
		$button.hide();
		$loading.show();
		
		currentPage += 1;
		$.ajax({
			url: "/api/images/page/" + currentPage,
			success: function (data) {
				var images = data.IMAGES;
				var imageHTML = "";
				if (images.length > 0) {
					for (var i = 0; i < images.length; i++) {
						imageHTML += Mustache.render(imageTemplate, images[i]);
					}
				}
				else{
					$button.hide();
				}
				$("#imageContainer").append(imageHTML);
				
				$button.show();
				$loading.hide();
			}
		});
		
		
		var buttonText;
		switch (currentPage % 4) {
		case 0:
			buttonText = "Show me more!";
			break;
		case 1:
			buttonText = "Keep 'em coming!";
			break;
		case 2:
			buttonText = "I'd like s'more.";
			break;
		case 3:
			buttonText = "More more more...";
			break;
		}
		$button.text(buttonText);
		
	});
	
}());