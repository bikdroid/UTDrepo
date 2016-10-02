/*Chatbox Javascript*/
$(document).ready(function(){


	 var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                console.log('appended');
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
	sendMessage = function(text){

	}
	$(".send_message").click(function(){

		var $message_input, $messages, message, message_side;
		$message_input = $('.message_input');
		
		$messages = $('.messages');
		message_side = 'right';
		message_side = message_side === 'left'?'right':'left';

		message = new Message({
			text: text,
			message_side: message_side
		});
		$('.messages').append($message_input.val() + "\n");
		console.log($message_input.val());
		console.log("button clicked !!");

	});
})