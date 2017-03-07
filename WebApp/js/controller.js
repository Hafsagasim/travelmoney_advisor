/**
 * Created by Laszlo Szoboszlai on 26/02/2017.
 */
var currencies ={};
var keys = [];
var HOST = '127.0.0.1';
var PORT = '5000';
var URL = "http://" + HOST + ":" + PORT;

$( document ).ready(function() {
    $("#result").hide();
	$("#progressbar").hide();

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": URL +"/currencies",
        "method": "GET",
        "headers": {
            "cache-control": "no-cache",
            "postman-token": "43402fbd-0e3f-3d93-03ab-4f22eaf1f810"
        },
        "data": "{ \n  \"currency\" : \"EUR\",\n    \"days\": 5\n}"
    }

    $.ajax(settings).done(function (response) {
        for(var key in response){
            $('#from').append( '<li><a href="#"><id=' + key + '">' + key + '</a></li>' );
        }

            $("#from li a").click(function(){
                $("#fromDropdownMenu:first-child").text($(this).text());
                $("#fromDropdownMenu:first-child").val($(this).text());
				$("#todr").empty();
				$("#toDropdownMenu:first-child").text('Currency to');
				$("#toDropdownMenu:first-child").val('');

                var curr = ($("#fromDropdownMenu:first-child").val())
                var settings = {
					"async": true,
					"crossDomain": true,
					"url": URL+ "/tocurrencies",
					"method": "POST",
					"headers": {
						"content-type": "application/json",
						"currency": "\""  + curr + "\"",
						"cache-control": "no-cache",
						"postman-token": "d71648ba-61f2-5293-e424-ec45e85ed4c7"
						},
					"processData": false,
					"data": "{ \n  \"currency\" : \"" + curr + "\" \n}"
				}

                $.ajax(settings).done(function (response) {
					for(var key2 in response){
						$('#todr').append( '<li><a href="#"><id=' + key2 + '">' + key2 + '</a></li>' );

						}
                    $("#todr li a").click(function(){
                        $("#toDropdownMenu:first-child").text($(this).text());
                        $("#toDropdownMenu:first-child").val($(this).text());
                    });
            });
        });
    });

    });

function movebar(){
	var elem = document.getElementById("bar");
	var width = 1;
	var id = setInterval(frame, 13);
	
	function frame(){
		if (width>= 100){
			clearInterval(id);
		} else{
				width++;
				elem.style.width = width + '%';
				elem.innerHTML = width * 1 + '%';
			}
	}
}

$("#days li a").click(function(){
    $("#daysDropdownMenu:first-child").text($(this).text());
    $("#daysDropdownMenu:first-child").val($(this).text());
});

$("#forecast").click(function(){
	$("#progressbar").show();
	movebar();
    var currfrom = ($("#fromDropdownMenu:first-child").val());
	var currto = ($("#toDropdownMenu:first-child").val());
    var days = ($("#daysDropdownMenu:first-child").val());
    var settings = {
		"async": true,
		"crossDomain": true,
		"url": URL + "/forecast",
		"method": "POST",
		"headers": {
			"content-type": "application/json",
			"cache-control": "no-cache",
			"postman-token": "d0134958-b639-0d25-f0a6-838ca556c7e9"
			},
		"processData": false,
        "data": "{\n \"currencyfrom\": \"" + currfrom + "\",\n \"currencyto\": \"" + currto + "\",\n \"days\":"+days + "\n}"
		}

	$.ajax(settings).done(function (response) {
		var data = response['forecasts'];
		$("#result").text('According to the forecast the best day to buy is: ' + response['tobuy'] + ' and to sell is: ' + response['tosell']);
		$("#result").fadeIn();

        Morris.Line({
            element: 'placeholder',
            data: data,
			ymin: 'auto',
            xkey: 'x',
            ykeys: ['y'],
            labels: ['value']
        });
		});
});
