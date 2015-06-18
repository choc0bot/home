
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

$(function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 1440,
      step: 15,
      values: [ 60, 480 ],
      slide: function( event, ui ) {
            var hours1 = Math.floor(ui.values[0] / 60);
            var minutes1 = ui.values[0] - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            var hours2 = Math.floor(ui.values[1] / 60);
            var minutes2 = ui.values[1] - (hours2 * 60);

            if(hours2.length < 10) hours2= '0' + hours;
            if(minutes2.length < 10) minutes2 = '0' + minutes;

            if(minutes2 == 0) minutes2 = '00';

            jQuery('#on').val(hours1+':'+minutes1);
            jQuery('#off').val(hours2+':'+minutes2 );
        }
    });
});


$(function() {
    $( "#slider-range-min" ).slider({
      range: "min",
      value: 90,
      min: 0,
      max: 600,
      step: 15,
      slide: function( event, ui ) {
            var hours1 = Math.floor(ui.value / 60);
            var minutes1 = ui.value - (hours1 * 60);

            if(hours1.length < 10) hours1= '0' + hours;
            if(minutes1.length < 10) minutes1 = '0' + minutes;

            if(minutes1 == 0) minutes1 = '00';

            jQuery('#amount').val(hours1+':'+minutes1);
      }
    });
});
