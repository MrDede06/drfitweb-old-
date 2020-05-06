var tlist = [];
$("#tlist").val('');

var enlist = [];
$("#enlist").val('');

var fllist = [];
$("#fllist").val('');

var delist = [];
$("#delist").val('');

var eslist = [];
$("#eslist").val('');

$("#addnewstitle").click(function (){
var altyazi = $("#altyazi").val();
console.log(altyazi);
$("#subtitlelist").append('<div class="alert alert-success">'+
  '<i class="fa fa-check fa-lg"></i><strong>'+ altyazi +'</strong>'+
'</div>')
$("#altyazi").val('');
tlist.push(altyazi);
var test = JSON.stringify(tlist);
$("#tlist").val(test);
});

$("#addnewentitle").click(function (){
var altyazien = $("#altyazien").val();
console.log(altyazien);
$("#subtitlelisten").append('<div class="alert alert-success">'+
  '<i class="fa fa-check fa-lg"></i><strong>'+ altyazien +'</strong>'+
'</div>')
$("#altyazien").val('');
enlist.push(altyazien);
var testen = JSON.stringify(enlist);
$("#enlist").val(testen);
});


$("#addnewfltitle").click(function (){
var altyazifl = $("#altyazifl").val();
console.log(altyazifl);
$("#subtitlelistfl").append('<div class="alert alert-success">'+
  '<i class="fa fa-check fa-lg"></i><strong>'+ altyazifl +'</strong>'+
'</div>')
$("#altyazifl").val('');
fllist.push(altyazifl);
var testfl = JSON.stringify(fllist);
$("#fllist").val(testfl);
});


$("#addnewdetitle").click(function (){
var altyazide = $("#altyazide").val();
console.log(altyazide);
$("#subtitlelistde").append('<div class="alert alert-success">'+
  '<i class="fa fa-check fa-lg"></i><strong>'+ altyazide +'</strong>'+
'</div>')
$("#altyazide").val('');
fllist.push(altyazide);
var testde = JSON.stringify(delist);
$("#delist").val(testde);
});


$("#addnewestitle").click(function (){
var altyazies = $("#altyazies").val();
console.log(altyazies);
$("#subtitlelistes").append('<div class="alert alert-success">'+
  '<i class="fa fa-check fa-lg"></i><strong>'+ altyazies +'</strong>'+
'</div>')
$("#altyazies").val('');
eslist.push(altyazies);
var testes = JSON.stringify(eslist);
$("#eslist").val(testes);
});


$("#addnewvideo").click(function (){
Messenger().post({
        message: "Video Yükleniyor lütfen bekleyin..",
        type: 'error',
        showCloseButton: true
   });


     var formData = new FormData($("#kateform")[0]);
     var datastring = $("#kateform").serialize();


$.ajax({
 type: "POST",
 url: "http://drfit.training/addnv/",
 data: formData,
 async: false,
 cache: false,
 contentType: false,
 processData: false,
 success: function(msg) {

     if (msg["response"] == "ok") {
       Messenger().post("Video Başarı ile eklendi");
       location.reload(true)


     }else{

       Messenger().post(msg["message"]);
     }
 },
 error: function(e) {
     console.log(e);
     alert('error handing here');
 }
});

});
