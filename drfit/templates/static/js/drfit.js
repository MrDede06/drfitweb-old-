$(document).ready(function() {
var ourindex = 0;
$('#myCombobox').combobox();
//$('#videoBelirle').combobox();
$("#videoBelirle").select2();


$('#videocombo').combobox({autoResizeMenu: false});
var selectedvideo = "Forward to Backward Lunge";
var cateid = "";
var subcateid = "";
var videoid = "74";

$('#videocombo').on('changed.fu.combobox', function (evt, data) {
selectedvideo =  data["text"];
console.log(selectedvideo);
console.log(data);

});

$('#myWizard').on('finished.fu.wizard', function (evt, data) {
	// do something
  console.log("everyting are ok");
  location.reload(true);
});





$("#createpro").click(function (){
var setsayisi = $("#setsayisix").val();
var tekrarsaytisi = $("#tekrarsayisix").val();
var isitduration = $('#isitduration:checked').val();
console.log(isitduration);
if (cateid == "" || subcateid == "" || videoid == "") {
  location.reload(true);
} else {

  if(setsayisi.length <= 0 || tekrarsaytisi.length <= 0){
    alert("Lütfen set sayısı ve tekrar sayısı belirleyin");
  } else if(parseInt(setsayisi) > 4){
    alert("Set sayısı maximum 4 olabilir.");
  } else {
ourindex = ourindex +1;
$('#myWizard').wizard('addSteps', ourindex, [
	{
		badge: ourindex,
		label: ourindex + '. Adım',
		pane: '<div>'+setsayisi+' Set ve '+tekrarsaytisi+' tekrardan oluşan <b>'+selectedvideo+'</b> isimli video başarıyla eklendi.</div>'
	}
]);
$('#myWizard').wizard('selectedItem', {
	step: ourindex
});



    $.ajax({
      type:'POST',
      url:'http://drfit.training/addnewstep/',
      data:{cateid: cateid, subcateid:subcateid, videoid:videoid, tekrarsaytisi:tekrarsaytisi , setsayisi:setsayisi,isitduration:isitduration},
      success:function(msg){
        console.log(msg);
        if (msg["response"] == "ok") {
            Messenger().post("Great!");
        }else{
        Messenger().post(msg);
        }
      },
});
}
}

});





$("#creterest").click(function (){
var resttime = $("#resttime").val();
if (cateid == "" || subcateid == "") {
  location.reload(true);
} else {
  console.log(resttime.length);
  if(resttime.length <= 0){
    alert("Lütfen dinlenme süresi belirleyin");
  } else {
    console.log("tıklandı");
    ourindex = ourindex +1;
    var resttime = $("#resttime").val();
    $('#myWizard').wizard('addSteps', ourindex, [
      {
        badge: ourindex,
        label: 'Rest',
        pane: '<div>'+resttime+' saniye dinlenme eklendi.</div>'
      }
    ]);
    $('#myWizard').wizard('selectedItem', {
      step: ourindex
    });


    $.ajax({
      type:'POST',
      url:'http://drfit.training/addnewstep/',
      data:{cateid: cateid, subcateid:subcateid,resttime:resttime},
      success:function(msg){
        console.log(msg);
        if (msg["response"] == "ok") {
            Messenger().post("Great!");
        }else{

        Messenger().post(msg);


        }
      },
    });
  }
}
});



$('#mySubCombobox').on('changed.fu.combobox', function (evt, data) {
subcateid =  data["value"];
});

$('#videoBelirle').on('select2:select', function(e) {
    data = e.params.data;
    videoid = data.id;
    selectedvideo = data.text;
    console.log(videoid);
});



$('#myCombobox').on('changed.fu.combobox', function (evt, data) {
cateid =  data["value"];

$.ajax({
      type:'POST',
      url:'/getsubcates/',
      data:{cateid: cateid},
      success: function(msg) {
          console.log(msg);
          if (msg["response"] == "ok") {

            if (msg["subcatearr"].length > 0) {
              $("#subcts").html("")
              $.each(msg["subcatearr"], function( index, value ) {
                //$("#subcts").append("<option value="+value[0]+">"+value[1]+"</option>");

                $("#subcts").append('<li data-value='+value[0]+'><a href="#">'+value[1]+'</a></li>');
                $('#mySubCombobox').combobox('enable');

              });

            //$("#hlist").show("slow");
          }else {

            alert("Önce Alt kategori ekleyin.");
            $('#mySubCombobox').combobox('disable');
            }


          }else{

            Messenger().post(msg["response"]);
          }
      },
      error: function(e) {
          console.log(e);
          alert('error handing here');
        }
 });

 });


});
