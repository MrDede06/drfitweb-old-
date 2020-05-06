$('#hedefbox').combobox();
$('#alanbox').combobox();
$('#kilobox').combobox();
$('#powerbox').combobox();
$('#daytypebox').combobox();
$('#whichweekbox').combobox();
$('#selectdaybox').combobox();
$("#videobox").select2();

var ourindex = 0;
var nextnextpls = "firstDay";
var selectedvideo = "Forward to Backward Lunge";

var hedef = "";
var calismaalani = "";
var kilotipi = "";
var guctipi = "";
var guntipi = "";
var videoid = "74";
var whichweek = "";
var whichday = "";



 $('#alanbox').on('changed.fu.combobox', function (evt, data) {
calismaalani =  data["value"];
 });

 $('#kilobox').on('changed.fu.combobox', function (evt, data) {
kilotipi =  data["value"];
 });
 $('#powerbox').on('changed.fu.combobox', function (evt, data) {
guctipi =  data["value"];
 });

 $('#selectdaybox').on('changed.fu.combobox', function (evt, data) {
whichday =  data["value"];
ourindex=0;
 });


 $('#whichweekbox').on('changed.fu.combobox', function (evt, data) {
whichweek =  data["value"];
$("#firstDaySteps").html("");
$("#firstDayStepsContent").html("");

$("#secondDaySteps").html("");
$("#secondDayStepsContent").html("");

$("#thirdDaySteps").html("");
$("#thirdDayStepsContent").html("");

$("#fourthDayDaySteps").html("");
$("#fourthDayStepsContent").html("");

$("#lastdaySteps").html("");
$("#lastdayStepsContent").html("");

 });



 $('#videobox').on('select2:select', function(e) {
data = e.params.data;
videoid =  data.id;
selectedvideo = data.text;
 });




$('#hedefbox').on('changed.fu.combobox', function (evt, data) {
hedef = data["value"];
console.log(hedef);
$("#alanboxsub").html("")
if (parseInt(hedef) == 3) {
  console.log("3ü seçtiniz");
  $("#alanboxsub").append('<li data-value="2"><a href="#">Freeweight</a></li>');
  $('#alanbox').combobox('enable');
} else {
  $("#alanboxsub").append('<li data-value="1"><a href="#">Body weight</a></li>');
  $("#alanboxsub").append('<li data-value="2"><a href="#">Free weight</a></li>');

  $('#alanbox').combobox('enable');
}
});


$('#daytypebox').on('changed.fu.combobox', function (evt, data) {
guntipi =  data["value"];
$("#selectdaysub").html("");
if (parseInt(guntipi) == 3) {
  console.log("3ü seçtiniz");
  $("#selectdaysub").append('<li data-value="1"><a href="#">1. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="2"><a href="#">2. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="3"><a href="#">3. Gün</a></li>');
  $('#selectdaybox').combobox('enable');
} else if(parseInt(guntipi) == 4) {
  $("#selectdaysub").append('<li data-value="1"><a href="#">1. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="2"><a href="#">2. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="3"><a href="#">3. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="4"><a href="#">4. Gün</a></li>');
  $('#selectdaybox').combobox('enable');
} else if(parseInt(guntipi)== 5) {
  $("#selectdaysub").append('<li data-value="1"><a href="#">1. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="2"><a href="#">2. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="3"><a href="#">3. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="4"><a href="#">4. Gün</a></li>');
  $("#selectdaysub").append('<li data-value="5"><a href="#">5. Gün</a></li>');
  $('#selectdaybox').combobox('enable');
}else{
  alert("Bir sorun olştu");
}
});




$("#createpro").click(function (){
  var setsayisi = $("#setsayisix").val();
  var totaltime = $("#totaltime").val();
  var tekrarsaytisi = $("#tekrarsayisix").val();

  if (whichday==1) {nextnextpls="firstDay";}
  else if(whichday==2){nextnextpls="secondDay";}
  else if(whichday==3){nextnextpls="thirdDay";}
  else if(whichday==4){nextnextpls="fourthDay";}
  else if(whichday==5){nextnextpls="lastday";}

if (hedef == "" || calismaalani == "" || guctipi == "" || guntipi == "" || videoid == "" || whichweek == "" || whichday == "") {

  console.log("hedef" + hedef);
  console.log("calismaalani" + calismaalani);
  console.log("kilotipi" + kilotipi);
  console.log("guctipi" + guctipi);
  console.log("videoid" + videoid);
  console.log("whichweek" + whichweek);
  console.log("whichday" + whichday);

  //location.reload(true);
} else {

  if(setsayisi.length <= 0 || totaltime.length <= 0 || tekrarsaytisi.length <= 0 || hedef.length <= 0 || calismaalani.length <= 0 || guctipi.length <= 0 || guntipi.length <= 0 || videoid.length <= 0 || whichweek.length <= 0 || whichday.length <= 0){
    Messenger().post("Lütfen her şeyi seçtiğine emin olun");
  } else if(parseInt(setsayisi) > 4){
    alert("Set sayısı maximum 4 olabilir.");
  } else {
ourindex = ourindex +1;
$('#'+nextnextpls).wizard('addSteps', ourindex, [
	{
		badge: ourindex,
		label: ourindex + '. Adım',
		pane: '<div>'+calismaalani+' Set ve '+hedef+' tekrardan oluşan <b>'+selectedvideo+'</b> isimli video başarıyla eklendi.</div>'
	}
]);
$('#'+nextnextpls).wizard('selectedItem', {
	step: ourindex
});

var isitduration = $('#isitduration:checked').val();
console.log(isitduration);
//startify*-*-*-*-*
$.ajax({
  type:'POST',
  url:'http://drfit.training/addnewbstep/',
  data:{hedef: hedef, calismaalani:calismaalani,kilotipi:kilotipi, guctipi:guctipi, guntipi:guntipi, videoid:videoid, whichweek:whichweek, whichday:whichday, tekrarsaytisi:tekrarsaytisi , setsayisi:setsayisi, totaltime:totaltime,isitduration:isitduration},
  success:function(msg){
    console.log(msg);
    if (msg["response"] == "ok") {
        Messenger().post("Great!");
    }else{

    Messenger().post(msg);


    }
  },
});

//stopify-*-*-*






}
}

});










$("#creterest").click(function (){
var resttime = $("#resttime").val();
if (whichday==1) {nextnextpls="firstDay";}
else if(whichday==2){nextnextpls="secondDay";}
else if(whichday==3){nextnextpls="thirdDay";}
else if(whichday==4){nextnextpls="fourthDay";}
else if(whichday==5){nextnextpls="lastday";}


if (hedef == "" || calismaalani == "" || guctipi == "" || guntipi == "" || videoid == "" || whichweek == "" || whichday == "") {
  location.reload(true);
} else {
  console.log(resttime.length);
  if(resttime.length <= 0){
    alert("Lütfen dinlenme süresi belirleyin");
  } else {
    console.log("tıklandı");
    ourindex = ourindex +1;
    var resttime = $("#resttime").val();
    $('#'+nextnextpls).wizard('addSteps', ourindex, [
      {
        badge: ourindex,
        label: 'Rest',
        pane: '<div>'+resttime+' saniye dinlenme eklendi.</div>'
      }
    ]);
    $('#'+nextnextpls).wizard('selectedItem', {
      step: ourindex
    });




    //startify*-*-*-*-*
    $.ajax({
      type:'POST',
      url:'http://drfit.training/addnewbstep/',
      data:{hedef: hedef, calismaalani:calismaalani,kilotipi:kilotipi, guctipi:guctipi, guntipi:guntipi, videoid:videoid, whichweek:whichweek, whichday:whichday, resttime:resttime },
      success:function(msg){
        console.log(msg);
        if (msg["response"] == "ok") {
            Messenger().post("Great!");
        }else{

        Messenger().post(msg);


        }
      },
    });

    //stopify-*-*-*
  }
}
});
