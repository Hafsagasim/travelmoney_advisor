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