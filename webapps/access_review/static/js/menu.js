$(document).ready(function()
{
	console.log("1");
    $("#button_addnew_1").click(function()
    {
    	  console.log("here");
          $("#div_addnew_1").show();
          $("#div_addnew_1").attr("visible", true);
    });
});

$(document).ready(function()
{
	console.log("1");
    $("#done_1").click(function()
    {
    	  console.log("in done");
          $("#div_addnew_1").attr("visible", false);
    });
});


$(document).ready(function()
{
    $("#button_edit_1").click(function()
    {
          $(this).hide();
          $("#div_edit_1").show();
    });
});
