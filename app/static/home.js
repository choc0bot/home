
$("#lounge").click(function(){
    $.get("/testlounge",
    function(data){
        if(data='ON'){
              $("#lounge").toggleClass("btn-danger btn-success");
          }
    })
});

$("#bed1").click(function(){
    $.get("http://192.168.1.101/cgi-bin/relay.cgi?toggle",
    function(data){
        if(data='ON'){
            $("#bed1").toggleClass("btn-danger btn-success");
          }
    })
});

$("#bed2").click(function(){
$.get("/testbed2",
    function(data){
        if(data='ON'){
            $("#bed2").toggleClass("btn-danger btn-success");
          }
    })
});

$("#refresh").click(function(){
location.reload();
});

function timeNow() {
  var d = new Date(),
      h = (d.getHours()<10?'0':'') + d.getHours(),
      m = (d.getMinutes()<10?'0':'') + d.getMinutes();
      i = h + ':' + m;
      return i;
}

function addtime(timestring) {
    var res = timestring.split(":")
    var hour = res[0];
    var min = res[1];
    var dateT = new Date();
    hour = hour.replace(/^0+/, '');
    d = new Date(dateT.getTime() + res[0]*3600000 + res[1]*60000);
    h = (d.getHours()<10?'0':'') + d.getHours(),
    m = (d.getMinutes()<10?'0':'') + d.getMinutes();
    i = h + ':' + m;
    return i;

}

$(".addtimer").click(function() {
        var spanHighValue = $(this).closest(".timer-value").text()
        alert(timerValue);
        var curtime = timeNow(),
            //spanHighValue = $('#slider-step-value').text();
        endtime = addtime(spanHighValue);

        $.post( '/add_timer', { starttime: curtime, endtime: endtime } )
        .done(function( data ) {
        location.reload();
        });
});

$("#adder").click(function() {

        var spanLowValue  = $('#slider-range-noui-value-start').text(),
            spanHighValue = $('#slider-range-noui-value-end').text();

        $.post( '/add_timer', { starttime: spanLowValue, endtime: spanHighValue } )
        .done(function( data ) {
        location.reload();
        });
});

$('.btn-delete').click(function() {
  $(this).closest("div").remove()
  var deleteid = this.dataset.id;
  //alert(deleteid);
  //var form = $('<form action="/delete_timer/' + this.dataset.id + '" method="post"></form>');
  //form.submit();
  $.post( '/delete_timer/' + deleteid)

});

/*
function pad(a){
    return a < 10 ? '0'+a : a;
}

function set (value) {
    $(this).html(pad(Math.floor(value/4)) + ":" + pad((value%4)*15));
}

$(function() {
  var slider = $("#slider-step"), val = $("#slider-step-value");

  slider.noUiSlider({
      range: { min: 0, max: (12*4) },
      start: 8
  });

  slider.Link().to(val, set, wNumb({ decimals: 0 }));
});

$(function() {
  var sliderrangenoui = $("#slider-range-noui"),
      valstart = $("#slider-range-noui-value-start"),
      inputstart = $('#input-start'),
      inputend = $('#input-end'),
      valend = $("#slider-range-noui-value-end");

  sliderrangenoui.noUiSlider({
      range: { min: 0, max: (24*4) },
      start: [ 8, 48 ],
  });

  sliderrangenoui.Link('lower').to(valstart, set, wNumb({ decimals: 0 }));
  sliderrangenoui.Link('upper').to(valend, set, wNumb({ decimals: 0 }));

});
*/