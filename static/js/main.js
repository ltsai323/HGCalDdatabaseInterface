$(function () {

	'use strict';

	// Form




	var PyTestGet = function () {
		/* my test Get Function */
		var $PyBtnGet = $("#PyBtnGet");
		var $PyBtnPost = $("#PyBtnPost");
		var $PyConsole = $("#PyConsole");

		var $varname = $("#name");
		var $varemail = $("#email");
		var $varphone = $("#phone");
		var $varcompany = $("#company");

		$PyBtnGet.off('click').on('click', function () {
			$.ajax({
				url: '/data/message',
				data: {},
				type: 'GET',
				success: function (data) {
					$PyConsole.text("");
					$PyConsole.append("data[name] : " + data.appInfo.name + "<br>");
					$PyConsole.append("data[email] : " + data.appInfo.email + "<br>");
					$PyConsole.append("data[phone] : " + data.appInfo.phone + "<br>");
					$PyConsole.append("data[company] : " + data.appInfo.company + "<br>");
					$varname.val(data.appInfo.name);
					$varemail.val(data.appInfo.email);
					$varphone.val(data.appInfo.phone);
					$varcompany.val(data.appInfo.company);
				},
				error: function (xhr) {
					alert("ajax request failed found");
				}
			});
		})
		/* my test Get Function End */
	};

	var PyTestPost = function () {
		var $PyBtnGet = $("#PyBtnGet");
		var $PyBtnPost = $("#PyBtnPost");
		var $PyConsole = $("#PyConsole");

		var $varname = $("#name");
		var $varemail = $("#email");
		var $varphone = $("#phone");
		var $varcompany = $("#company");
		/* my test Post Function */
		$PyBtnPost.off('click').on('click', function () {
			$.ajax({
				url: '/data/message',
				data: {
					'name': $varname.val(),
					'email': $varemail.val(),
					'phone': $varphone.val(),
					'company': $varcompany.val()
				},
				type: 'POST',
				success: function (data) {
					$PyConsole.text("result = ");
					$PyConsole.append(data.result);

				},
				error: function (xhr) {
					alert("ajax request failed found");
				}
			});
		})
		/* my test Post Function End */
	};

	var contactForm = function () {
		var $varname = $("#name");
		var $varemail = $("#email");
		var $varphone = $("#phone");
		var $varcompany = $("#company");
		if ($('#contactForm').length > 0) {
			$("#contactForm").validate({
				rules: {
					name: "required",
					email: {
						required: true,
						email: true
					},
					message: {
						required: true,
						minlength: 5
					}
				},
				messages: {
					name: "Please enter your name",
					email: "Please enter a valid email address",
					message: "Please enter a message"
				},
				// submit via ajax
				submitHandler: function (form) {
					var $submit = $('.submitting'),
						waitText = 'Submitting...';

					$.ajax({
						type: "POST",
						url: '/data/message',
						data: {
							'name': $varname.val(),
							'email': $varemail.val(),
							'phone': $varphone.val(),
							'company': $varcompany.val()
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
	//contactForm();

	PyTestGet();
});
