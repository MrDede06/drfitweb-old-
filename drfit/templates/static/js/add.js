$("#kategoriekle").click(function (){


    Messenger().post({
            message: "Kategori oluşturuluyor lütfen bekleyin..",
            type: 'error',
            showCloseButton: true
       });


       var formData = new FormData($("#kateform")[0]);
       var datastring = $("#kateform").serialize();


  $.ajax({
   type: "POST",
   url: "http://drfit.training/addcategoryfy/",
   data: formData,
   async: false,
   cache: false,
   contentType: false,
   processData: false,
   success: function(msg) {

       if (msg["response"] == "ok") {
         Messenger().post("kategori Başarı ile eklendi");
         location.reload(true);


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


$('#myCombobox').combobox();

$('#myCombobox').on('changed.fu.combobox', function (evt, data) {
var cateid =  data["value"];
console.log(cateid);
$("#cateforalt").val(cateid);
});


$('#alanbox').combobox();

var calismaalani = "";
$('#alanbox').on('changed.fu.combobox', function (evt, data) {
calismaalani =  data["value"];
console.log(calismaalani);
$("#calismaalanialt").val(calismaalani);
});



$("#altkategoriekle").click(function (){


    Messenger().post({
            message: "Alt Kategori oluşturuluyor lütfen bekleyin..",
            type: 'error',
            showCloseButton: true
       });


       var formData = new FormData($("#kateform")[0]);
       var datastring = $("#kateform").serialize();


  $.ajax({
   type: "POST",
   url: "http://drfit.training/addaltcategoryfy/",
   data: formData,
   async: false,
   cache: false,
   contentType: false,
   processData: false,
   success: function(msg) {

       if (msg["response"] == "ok") {
         Messenger().post("Alt kategori Başarı ile eklendi");
         location.reload(true);


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
