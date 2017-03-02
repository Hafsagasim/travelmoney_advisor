/**
 * Created by Laszlo Szoboszlai on 26/02/2017.
 */
$( document ).ready(function() {
    $("#result").hide();
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://laszloszoboszlai.me:5000/currencies",
        "method": "GET",
        "headers": {
            "cache-control": "no-cache",
            "postman-token": "43402fbd-0e3f-3d93-03ab-4f22eaf1f810"
        },
        "data": "{ \n  \"currency\" : \"EUR\",\n    \"days\": 5\n}"
    }

    $.ajax(settings).done(function (response) {
        for(var key in response){
            $('#to').append( '<li><a href="#"><id=' + key + '">' + key + '</a></li>' );
            $('#from').append( '<li><a href="#"><id=' + key + '">' + key + '</a></li>' );
            console.log(key);
        }

        $(function(){
            $("#to li a").click(function(){

                $("#toDropdownMenu:first-child").text($(this).text());
                $("#toDropdownMenu:first-child").val($(this).text());


            });
        });

        $(function(){

            $("#from li a").click(function(){
                $("#fromDropdownMenu:first-child").text($(this).text());
                $("#fromDropdownMenu:first-child").val($(this).text());
            });
        });
        //console.log(response);
    });
});

/*
$(function(){

    $("#from li a").click(function(){
        $("#fromDropdownMenu:first-child").text($(this).text());
        $("#fromDropdownMenu:first-child").val($(this).text());
    });
});
*/


$("#days li a").click(function(){

    $("#daysDropdownMenu:first-child").text($(this).text());
    $("#daysDropdownMenu:first-child").val($(this).text());


});

$("#forecast").click(function(){
    var curr = ($("#fromDropdownMenu:first-child").val())
    var days = ($("#daysDropdownMenu:first-child").val())
    var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://laszloszoboszlai.me:5000/forecast",
  "method": "POST",
  "headers": {
    "content-type": "application/json",
    "cache-control": "no-cache",
    "postman-token": "d0134958-b639-0d25-f0a6-838ca556c7e9"
  },
  "processData": false,
        "data": "{ \n  \"currency\" : \"" + curr + "\",\n    \"days\":"+days + "\n}"
    }

 //settings.add( ['data'] = "{currency: "+ curr + ",  days: " + days + "}" );
$.ajax(settings).done(function (response) {
  console.log(days);

    $("#result").text(response['forecasts']);
    $("#result").fadeIn();
});


//    if ($("#fromDropdownMenu:first-child").val() == "");
//
//   alert($("#fromDropdownMenu:first-child").val() + " " + $("#toDropdownMenu:first-child").val());
//  console.log('forecast clicked');

});