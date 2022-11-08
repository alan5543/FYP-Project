$("#toggleBtn").click(function () {
    if($('#paragraph').css('display') == 'none')
    {
        $("#toggleBtn").text("Show Entity");
        $("#paragraph-highlight").hide();
        $("#paragraph").show();
        $('#search-key').show();
        $('#search-btn').show();
    }
    else{
        $("#toggleBtn").text("Show Summary");
        $("#paragraph").hide();
        $("#paragraph-highlight").show();
        $('#search-key').hide();
        $('#search-btn').hide();
    }
  });