/**
 * Created by laci on 26/02/2017.
 */
$(function(){

    $("#from li a").click(function(){
        $("#fromDropdownMenu:first-child").text($(this).text());
        $("#fromDropdownMenu:first-child").val($(this).text());
    });
});

$(function(){
    $("#to li a").click(function(){

        $("#toDropdownMenu:first-child").text($(this).text());
        $("#toDropdownMenu:first-child").val($(this).text());

    });
});

$("#forecast").click(function(){
var settings = {
  "async": true,
  "crossDomain": true,
   "Access-Control-Allow-Origin" : "http://laszloszoboszlai.me",
  "url": "http://laszloszoboszlai.me:5000/currencies",
  "method": "GET",
  "headers": {
    "content-type": "application/json",
    "cache-control": "no-cache",
    "postman-token": "6f2090a9-f224-daf7-966e-1f6a90c2e79b"
  },
  "processData": true,
  "data": "{ \n  \"currency\" : \"EUR\",\n    \"days\": 5\n}"
}

$.ajax(settings).done(function (response) {
  console.log(response);
});
});