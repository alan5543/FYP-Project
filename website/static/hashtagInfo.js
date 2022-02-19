function debounce(func, wait, immediate) {
    var timeout;
    return function() {
      var context = this,
        args = arguments;
      var later = function() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      var callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) func.apply(context, args);
    };
  }
  
  var slider = document.getElementById("slider");
  var onScroll = debounce(function(direction) {
    //console.log(direction);
    if (direction == false) {
        $('.carousel-control-next').click();
    } else {
        $('.carousel-control-prev').click();
    }
  }, 100, true);
  
  if (slider){
    slider.addEventListener("wheel", function(e) {
        e.preventDefault();
        var delta;
        if (event.wheelDelta) {
          delta = event.wheelDelta;
        } else {
          delta = -1 * event.deltaY;
        }
      
        onScroll(delta >= 0);
      });
  }
