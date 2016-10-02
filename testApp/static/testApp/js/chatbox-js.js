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

	$(".send_message").click(function(){

		var $message_input, $messages, message, message_side, text;
		$message_input = $('.message_input');
		text = $('.message_input').val();
		console.log(text);
		$messages = $('.messages');
		message_side = 'right';
		message_side = message_side === 'left'?'right':'left';

		message = new Message({
			text: text,
			message_side: message_side
		});

		message.draw();
		console.log(message);
		// $.ajax({
		// 	url: "/testApp/chatbot/",
		// 	type: "POST",
		// 	data: { the_post : text},
		// 	success: function(json){
		// 		console.log(json);
		// 		console.log(success);
		// 	},
		// 	error: function(xhr,errmsg,err) {
            
  //           	console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
  //       	}
		// });
		// $.get('/testApp/querynlp',{'query':text}, function(data)
		// 	{
		// 		console.log('requesting server for query analysis');
		// 		message_side = message_side === 'left'?'right':'left';
		// 		message = new Message({
		// 			text: data['answer'],
		// 			message_side: message_side
		// 		});
		// 		console.log(data);	
		// 	});
		console.log("button clicked !!");

	});
})