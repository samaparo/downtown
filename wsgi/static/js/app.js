/*global $ */
/*global console */
var imageTemplate;
var currentPage = 0;
(function () {
	'use strict';
	currentPage = 0;
	imageTemplate = $("#template_image").html();
	
	$("#buttonWrapper button").click(function () {
		console.log("click");
	});
	
}());