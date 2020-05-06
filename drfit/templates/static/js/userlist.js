$(document).ready(function() {

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');




    $('#otel-datalist').DataTable( {

                "order": [[ 0, "desc" ]],
                "columnDefs": [
                { "width": "10%", "targets": 0 },
                { "width": "30%", "targets": 1 },
                { "width": "30%", "targets": 2 },
                { "width": "10%", "targets": 3 },
                { "width": "20%", "targets": 4 },



              ]


    } );



    $.ajax({
       type:'POST',
       url:'/getlastuyeler/',
       data:{csrfmiddlewaretoken:csrftoken},
       success:function(msg){
         console.log(msg);
    $('#otel-datalist').dataTable().fnClearTable();
         for(i in msg.response){
  //$("#table-body").append('<tr class="gradeX"><td>'+msg.response[i][0]+'</td><td>'+msg.response[i][1]+'</td><td>'+msg.response[i][2]+'</td></tr>');
    $('#otel-datalist').dataTable().fnAddData( [
      msg.response[i][0],
      msg.response[i][1],
      msg.response[i][2],
      msg.response[i][3],
      '<center><a target="_blank" href="http://drfit.training/admin/core/user/'+msg.response[i][0]+'/change/"><i class="fa fa-pencil"></i> Düzenle</a></center>'
      //  '<center><a href="/musteridetay/'+msg.response[i][0]+'"><i class="fa fa-pencil"></i> Düzenle</a></center>'
      ]
      );
        }
       }
  });




$("#otel-ara").click(function(){
var hotelname = $("#hotelname").val();
  $.ajax({
     type:'POST',
     url:'/searchmusteri/',
     data:{query: hotelname,csrfmiddlewaretoken:csrftoken},
     success:function(msg){
       console.log(msg);
  $('#otel-datalist').dataTable().fnClearTable();
       for(i in msg.response){
//$("#table-body").append('<tr class="gradeX"><td>'+msg.response[i][0]+'</td><td>'+msg.response[i][1]+'</td><td>'+msg.response[i][2]+'</td></tr>');
  $('#otel-datalist').dataTable().fnAddData( [
      msg.response[i][0],
      msg.response[i][1],
      msg.response[i][2],
      msg.response[i][3],
      '<center><a href="/musteridetay/'+msg.response[i][0]+'"><i class="fa fa-pencil"></i> Düzenle</a></center>'




    ]
    );
      }
     }
});
});





});
