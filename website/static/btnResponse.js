
  $(".btnLoading").click(function () {
    $(".contentContainer").hide();
    $(".loader-wrapper").show();
  });

  $(".sumBtn").click(function () {
    $(".waitingInfo").text("The summarizer may take 1-2 minutes");
    $(".contentContainer").hide();
    $(".loader-wrapper").show();
  });

  $(".analysisBtn").click(function () {
    $(".waitingInfo").text(
      "We are deep-analyzing the article structure now .."
    );
    $(".contentContainer").hide();
    $(".loader-wrapper").show();
  });

  $(".emotionBtn").click(function () {
    $(".waitingInfo").text("We are deep-analyzing the author emotion now ..");
    $(".contentContainer").hide();
    $(".loader-wrapper").show();
  });

    $(".twitterBtn").click(function () {
    $(".waitingInfo").text("We are finding the hashTag now ..");
    $(".contentContainer").hide();
    $(".loader-wrapper").show();
  });

  $(".dashboardBtn").click(function () {
    $(".waitingInfo").text("Backing to the Dashboard ..");
    $(".contentContainer").hide();
    $(".loader-wrapper").show();
  });
