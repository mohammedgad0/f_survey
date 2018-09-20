// number Validation
function check(e,value){
  //Check Charater
    var unicode=e.charCode? e.charCode : e.keyCode;
  if (value.indexOf(".") != -1)if( unicode == 46 )return false;
  if (unicode!=8)if((unicode<48||unicode>57)&&unicode!=46)return false;
}
// check length
function checkLength(el_id, max_length){
  var fieldLength = document.getElementById(el_id).value.length;
  //Suppose u want 4 number of character
  if(fieldLength <= max_length){
      return true;
  }
  else
  {
      var str = document.getElementById(el_id).value;
      str = str.substring(0, str.length - 1);
      document.getElementById(el_id).value = str;
  }
}

$('[data-toggle="tooltip"]').tooltip();
$('.tooltip-link, .tooltip-legend').on('click', function(){
  return false;
});
