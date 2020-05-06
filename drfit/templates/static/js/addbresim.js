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
   url: "http://drfit.training/addnewbimg/",
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
