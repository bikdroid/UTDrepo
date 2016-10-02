/*Chatbox Javascript*/
$(document).ready(function(){

	$(".send_message").click(function(){

		var $message_input, $messages, message;
		$message_input = $('.message_input');
		$messages = $('.messages');
		$('.messages').append($message_input.val());
		console.log($message_input.val());
		console.log("button clicked !!");

	});
})