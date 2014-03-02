/*global $ */
/*global console */
var imageTemplate;
var currentPage = 0;
(function () {
	'use strict';
	currentPage = 0;
	imageTemplate = $("#template_image").html();
	
	$("#buttonWrapper button").click(function () {
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
					$("#buttonWrapper button").hide();
				}
				$("#imageContainer").append(imageHTML);
				
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
		$("#buttonWrapper button").text(buttonText);
		
	});
	
}());