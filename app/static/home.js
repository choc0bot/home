
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
        var spanHighValue = $(this).closest("form").find(".timer-value").text();
        var deviceid = $(this).closest("form").find(".deviceid").attr('value');
        var endtime = addtime(spanHighValue);
        var timerType = 0;
        var curtime = timeNow();
        var timerclass = ".timer-div-"+ deviceid;
        $.post( '/add_timer', { starttime: curtime, endtime: endtime, deviceid: deviceid, timertype: timerType } )
        .done(function( data ) {
            //$(timerclass).append('<h3><label>on: </label><span class="label label-success">' + curtime + '</span> <label>off: </label><span class="label label-danger">' + endtime + '</span> <button class="btn-danger btn-delete btn-sm" data-id="temp-id"><span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span></button></h3>');
            $(timerclass).append('<div><span class="mdl-typography--caption">on:  </span><span class="mdl-typography--headline">' + curtime + '</span><span class="mdl-typography--text-right"><span class="mdl-typography--caption">off:  </span><span class="mdl-typography--headline">' + endtime + '</span></span><button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--accent btn-delete" data-id="'+deviceid+'"><i class="material-icons">clear</i></button></div>');
        //location.reload();
        });
});

$(".adder").click(function() {
        var spanLowValue = $(this).closest("form").find(".timer-low-value").text();
        var spanHighValue = $(this).closest("form").find(".timer-high-value").text();
        var deviceid = $(this).closest("form").find(".deviceid").attr('value');
        var timerType = 1;
        var timerclass = ".timer-div-"+ deviceid;
        $.post( '/add_timer', { starttime: spanLowValue, endtime: spanHighValue, deviceid: deviceid, timertype: timerType } )
        .done(function( data ) {
            //$(timerclass).append('<h3><label>on: </label><span class="label label-success">' + spanLowValue + '</span> <label>off: </label><span class="label label-danger">' + spanHighValue + '</span> <button class="btn-danger btn-delete btn-sm" data-id="temp-id"><span class="glyphicon glyphicon-minus-sign" aria-hidden="true"></span></button></h3>');
            $(timerclass).append('<div><span class="mdl-typography--caption">on:  </span><span class="mdl-typography--headline">' + spanLowValue + '</span><span class="mdl-typography--text-right"><span class="mdl-typography--caption">off:  </span><span class="mdl-typography--headline">' + spanHighValue + '</span></span><button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--accent btn-delete" data-id="'+deviceid+'"><i class="material-icons">clear</i></button></div>');
        //location.reload();
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