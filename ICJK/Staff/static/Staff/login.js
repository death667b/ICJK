$(document).ready(function(){
  $('ul.tabs').tabs();

// from https://stackoverflow.com/questions/19491336/get-url-parameter-jquery-or-how-to-get-query-string-values-in-js
  let params={};
  location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi,function(s,k,v){params[k]=v});
//

  if(params['result'] != undefined){
    let result = parseInt(params['result']);
    switch(result){
      case 0: // No error
      
      break;
      case 1: // invalid email
        M.toast({html: 'Your account creation failed because you used an invalid email address. Please try again.'});
      break;
      case 2: // Invalid password
        M.toast({html: 'Your account creation failed because you supplied an invalid password. Please try again.'});
      break;
      case 3: // Invalid confirm password
        M.toast({html: 'Your account creation failed because your password and confirmation did not match. Please try again.'});
      break;
      case 4: // Existing email
        M.toast({html: 'Your account creation failed because you used an email address that already exists. Please try again.'});
      break;
      default: // Unknown error
        M.toast({html: 'Your account creation failed because of an unknown error. Please try again.'});
      break;
    }
  }

});