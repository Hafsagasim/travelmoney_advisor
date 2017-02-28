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
  "url": "http://laszloszoboszlai.me:5000/forecast",
  "method": "POST",
  "headers": {
    "content-type": "application/json",
    "cache-control": "no-cache",
    "postman-token": "ebbeb938-9183-726c-f27e-96ffba2921cc"
  },
  "processData": false,
  "data": "{\n \"currency\":\"EUR\",\n \"days\":\"5\"\n}"
}

$.ajax(settings).done(function (response) {
  console.log(response);
});
});