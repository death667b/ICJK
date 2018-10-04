$(document).ready(function(){
  $('ul.tabs').tabs();

// from https://stackoverflow.com/questions/19491336/get-url-parameter-jquery-or-how-to-get-query-string-values-in-js
  let params={};
  location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi,function(s,k,v){params[k]=v});
//

  let view = 0
  if(params['view'] != undefined){
    let view_args = parseInt(params['view']);
    if(view_args == 0){
      view = 0;
    }else{
      view = 1;
    } 
  }

  if(view == 0){
    M.Tabs.getInstance(document.getElementById("login")).select();
  }else{
    M.Tabs.getInstance(document.getElementById("create")).select();
  }


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
      case 5:
        M.toast({html: 'Your account creation failed because of an unknown error. Please try again.'});
      break;
      case 6:
        M.toast({html: 'Your login failed because of an invalid email and password combination. Please try again.'});
      break;
      case 7:
        M.toast({html: 'Your login failed because of an unknown error. Please try again.'});
      break;
      default: // Unknown error
        M.toast({html: 'An unknown error has occurred. Please try again.'});
      break;
    }
  }

});