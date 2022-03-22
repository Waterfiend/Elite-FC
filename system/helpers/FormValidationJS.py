
def FormValidationErrorsJS(ids):
    return {
    'script':'''
        document.addEventListener('invalid', (function(){
            return function(e) {
            //prevent the browser from showing default error bubble / hint
            e.preventDefault();
            // optionally fire off some custom validation handler
            // myValidation();
            };
        })(), true);
        
        let ids =''' + str(ids) +
        '''
        let elements = []
        ids.forEach(function(id){
            elements.push(document.getElementById(id))
        })
        
        function DisplayErrors(element)
        {
                let oldErr = document.getElementById(element.id+'_err')
                if (oldErr)
                {
                    element.parentNode.removeChild(oldErr)
                }
                if(!element.checkValidity())
                {
                    let err = document.createElement("p")
                    err.id = element.id+'_err'
                    err.style.color = 'red'
                    console.log(element.value)
                    if(element.required&&element.value=='')
                    {
                        err.innerHTML = '*Field is Required'
                    }
                    else
                    {
                        err.innerHTML = element.title                       
                    }
                    element.parentNode.insertBefore(err,element.nextSibling) 
                }
                else
                {
                    let err = document.getElementById(element.id+'_err')
                    if(err)
                    {
                        element.parentNode.removeChild(err)
                    }
                }
        }
        
        elements.forEach(function(element){
            element.onchange = function(){
                DisplayErrors(element)
            }
        })
         document.getElementById('submit').onclick = function(){
            console.log('submit')
            elements.forEach(function(element){
                DisplayErrors(element)
            })     
        }
    '''
    }
def ConfirmPasswordErrorJS(passwordId,ConfirmPasswordId):
    return {
        'script':'''
            let password = document.getElementById('''+'"'+passwordId+'"'+')'+'\n'+
            '''let confirmPassword = document.getElementById('''+'"'+ConfirmPasswordId+'"'+')'+'\n'+
            '''let submit = document.getElementById('submit')
            let errList = []
            confirmPassword.oninput = function(){
                errList.forEach( function(err){
                    err.parentNode.removeChild(err)
                })
                errList = []
                if(confirmPassword.value!=password.value)
                {
                    submit.disabled = true;
                    let p = document.createElement("p");
                    p.style.color = 'red'
                    p.innerHTML = 'The password confirmation does not match'
                    errList.push(p)
                    confirmPassword.parentNode.insertBefore(p,confirmPassword.nextSibling)
                }
                else
                {
                    submit.disabled = false;    
                }
            }
        '''
    }

