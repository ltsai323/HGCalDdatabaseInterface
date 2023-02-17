$(function () {

	'use strict';

	// Form

	var contactForm = function () {
		var $input_vars = $("#input_vars");
		var $input_var2 = $("#input_var2");
		var $input_var3 = $("#input_var3");
		var $input_newvar = $("#input_newvar");
		var $input_name = $("#input_name");
		var $input_email = $("#input_email");
		var $input_message = $("#input_message");
		var $input_formatter = $("#input_formatter");
		var $input_locationid = $("#input_locationid");
		var $input_phone = $("#input_phone");
		var $input_company = $("#input_company");
		var $input_locationid = $("#input_locationid");

		var $input_PART_ID = $("#input_PART_ID");
		var $input_KIND_OF_PART_ID = $("#input_KIND_OF_PART_ID");
		var $input_LOCATION_ID = $("#input_LOCATION_ID");
		var $input_MANUFACTURER_ID = $("#input_MANUFACTURER_ID");
		var $input_RECORDED_INSERTION_USER = $("#input_RECORDED_INSERTION_USER");
		var $input_BARCODE = $("#input_BARCODE");
		var $input_COMMENT_DESCRIPTION = $("#input_COMMENT_DESCRIPTION");

		if ($('#contactForm').length > 0) {
			$("#contactForm").validate({
				rules: {
					input_name: "required",
					input_email: {
						required: true,
						email: true
					},
					input_message: {
						required: true,
						minlength: 5
					}
				},
				messages: {
					input_name: "Please enter your name",
					input_email: "Please enter a valid email address",
					input_message: "Please enter a message"
				},
				// submit via ajax
				submitHandler: function (form) {
					var $submit = $('.submitting'),
						waitText = 'Submitting...';

					$.ajax({
						type: "POST",
						url: '/data/message',
						data: {
							'records': {
								"input_vars": $input_vars.val(),
								"input_var2": $input_var2.val(),
								"input_var3": $input_var3.val(),
								"input_newvar": $input_newvar.val(),
								"input_name": $input_name.val(),
								"input_email": $input_email.val(),
								"input_message": $input_message.val(),
								"input_formatter": $input_formatter.val(),
								"input_locationid": $input_locationid.val(),
								"input_phone": $input_phone.val(),
								"input_company": $input_company.val(),
								"input_locationid": $input_locationid.val()
							},
							'basics': {
								"input_PART_ID": $input_PART_ID.val(),
								"input_KIND_OF_PART_ID": $input_KIND_OF_PART_ID.val(),
								"input_LOCATION_ID": $input_LOCATION_ID.val(),
								"input_MANUFACTURER_ID": $input_MANUFACTURER_ID.val(),
								"input_RECORDED_INSERTION_USER": $input_RECORDED_INSERTION_USER.val(),
								"input_BARCODE": $input_BARCODE.val(),
								"input_COMMENT_DESCRIPTION": $input_COMMENT_DESCRIPTION.val()
							}
						},

						beforeSend: function () {
							$submit.css('display', 'block').text(waitText);
						},
						success: function (msg) {
							if (msg.result == 'OK') {
								$('#form-message-warning').hide();
								setTimeout(function () {
									$('#contactForm').fadeOut();
								}, 1000);
								setTimeout(function () {
									$('#form-message-success').fadeIn();
								}, 1400);

							} else {
								$('#form-message-warning').html(msg.result);
								$('#form-message-warning').fadeIn();
								$submit.css('display', 'none');
							}
						},
						error: function () {
							$('#form-message-warning').html("Something went wrong. Please try again.");
							$('#form-message-warning').fadeIn();
							$submit.css('display', 'none');
						}
					});
				}

			});
		}
	};
	contactForm();

	//PyTestForm();
});
