/*Chatbox Javascript*/
$(document).ready(function(){



	 var Message;
	 var user_answer_required = 1;

	var entry_q = "Please specify last 4 digits of your account number. Thankyou";
    	setTimeout(function () {
				var message_side = message_side === 'left'?'right':'left';
				user_answer_required = 2;
				// console.log(data)
				message2 = new Message({
					text: entry_q,
					message_side: message_side
				});
				message2.draw();
				console.log('chat window load');
				console.log(message2);
				$('.messages').append(entry_q);
			},1000);

    Message = function (arg) {
        this.text = arg.text, this.message_side = 'left';//arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                console.log('appended');
                $('.messages').animate({ scrollTop: $('.messages').prop('scrollHeight') }, 300);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 1000);
            };
        }(this);
        return this;
    };

   //  $(".chat_window").load(function(){
   //  	var entry_q = "Please specify last 4 digits of your account number. Thankyou";
   //  	setTimeout(function () {
			// 	message_side = message_side === 'left'?'right':'left';
			// 	user_answer_required = 2;
			// 	// console.log(data)
			// 	message2 = new Message({
			// 		text: entry_q,
			// 		message_side: message_side
			// 	});
			// 	message2.draw();
			// 	console.log('chat window load');
			// 	console.log(message2);
			// 	$('.messages').append(entry_q);
			// },1000);

   //  });

	$(".send_message").click(function(){

		var $message_input, $messages, message, message_side, text;
		$message_input = $('.message_input');
		text = $('.message_input').val();
		console.log(text);
		
		 setTimeout(function () {
            $messages = $('.messages');
			message_side = 'right';
			//message_side = message_side === 'left'?'right':'left';

			message = new Message({
				text: text,
				message_side: message_side
			});

			message.draw();
			console.log(message);
			$('.messages').append($message_input.val());
        }, 1000);
/*		$messages = $('.messages');
		message_side = 'right';
		message_side = message_side === 'left'?'right':'left';

		message = new Message({
			text: text,
			message_side: message_side
		});

		message.draw();
		console.log(message);
		$('.messages').append($message_input.val());
*/		$.get('/testApp/querynlp/',{'the_post':text, 'user_ans':user_answer_required}, function(data)
			{
				console.log('requesting server for query analysis');
				setTimeout(function () {
				message_side = message_side === 'left'?'right':'left';
				user_answer_required = 1;
				console.log(data)
				message1 = new Message({
					text: data['result'],
					message_side: message_side
				});
				message1.draw();
				console.log(data);
				$('.messages').append(data['result']);
			},1000);
			});
		console.log($message_input.val());
		console.log("button clicked !!");

	});
})