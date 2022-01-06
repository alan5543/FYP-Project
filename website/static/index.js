function deleteNote(recordId) {
    console.log("Deleting the record now");
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ recordId: recordId }),
    }).then((_res) => {
      window.location.href = "/HKToday";
    });
    console.log("Finish the deletion");
  }

  function readNote(recordId) {
    console.log("Rereading the record now");
    fetch("/read-note", {
      method: "POST",
      body: JSON.stringify({ recordId: recordId }),
    }).then(function(_res){
        return _res.json();
    }).then(function(text) {
      console.log('GET Response: ');
      console.log(text.retitle);
      // redirect to the report dashboard with the parameters passing though URL
      window.location.href = "/newReport" + "?title=" + text.retitle + "&doc=" + text.retext;
    });
    console.log("Finish resending message");
  }
