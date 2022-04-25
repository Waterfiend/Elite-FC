
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

def DefineSubmitButtonChecksArray(size):
    return {
    'script':'''
        let submitChecks = Array('''+size+''')
    '''
    }
def FormValidateSumJS(total_id, other_ids, index):
    return {
    'script':'''
    (()=>{
        let index = '''+index+'''
        document.addEventListener('invalid', (function(){
            return function(e) {
            //prevent the browser from showing default error bubble / hint
            e.preventDefault();
            // optionally fire off some custom validation handler
            // myValidation();
            };
        })(), true);
        
        let other_ids =''' + str(other_ids) + 
        '''
        let total_id ='''+ '"'+total_id+'"'+
        
        '''
        let elements = []
        other_ids.forEach(function(id){
            elements.push(document.getElementById(id))
        })
        let total_element = document.getElementById(total_id)
        let submit = document.getElementById('submit')
        function DisplayErrors(element)
        {
                let oldErr = document.getElementById(total_element.id+'_err')
                if (oldErr)
                {
                    element.parentNode.removeChild(oldErr)
                }
                let requiredSum = parseInt(total_element.value)
                let currentSum = 0
                for (let i = 0; i< elements.length;i++)
                {
                    currentSum = currentSum + parseInt(elements[i].value)
                }
                console.log(currentSum)
                console.log(requiredSum)
                if(requiredSum<currentSum)
                {
                    let err = document.createElement("p")
                    err.id = total_element.id+'_err'
                    err.style.color = 'red'
                    console.log(element.value)
                    let values = ''
                    elements.forEach(function(element){
                        values = values + element.id.replace('_input','') + ','          
                    })
                    err.innerHTML = values + ' not adding up to '+total_element.id.replace('_input','')                      
                    total_element.parentNode.insertBefore(err,total_element.nextSibling)
                    submitChecks[index] = true
                     
                }
                else
                {
                    submitChecks[index] = false
                    let err = document.getElementById(total_element.id+'_err')
                    if(err)
                    {
                        total_element.parentNode.removeChild(err)
                    }
                }
                
                console.log(submitChecks)
                if (submitChecks.every(element => element === false))
                    submit.disabled = false;
                else
                    submit.disabled = true;
        }
        
        elements.forEach(function(element){
            let oldElementOnChange = element.onchange
            element.onchange = function(){
                DisplayErrors(element)
                oldElementOnChange()
                
            }
            
            
        })
        let oldTotalElementOnChange = total_element.onchange
        total_element.onchange = function(){
                oldTotalElementOnChange()
                elements.forEach(function(element){
                DisplayErrors(element)          
                })
                
                
        }
         document.getElementById('submit').onclick = function(){
            console.log('submit')
            elements.forEach(function(element){
                DisplayErrors(element)
            })     
        }
        })()
    '''
    }