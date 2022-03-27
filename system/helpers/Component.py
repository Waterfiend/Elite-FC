from xml.dom.minidom import Element
from django.middleware import csrf

class Component:
    def __init__(self,componenetType,options):
        self.componenetType = componenetType
        if (componenetType=='form'):
            self._initializeForm(options)
        elif (self.componenetType == 'table'):
            self._initializeTable(options)
        elif (self.componenetType == 'link'):
            self._initializeLink(options)
        elif (self.componenetType == 'script'):
            self._initializeScript(options)
        elif (self.componenetType == 'container'):
            self._initializeContainer(options)
            
    def create(self,request=None):
        if(self.componenetType=='form'):
            return self._createForm(request)
        if(self.componenetType=='table'):
            return self._createTable()
        if(self.componenetType=='link'):
            return self._createLink()
        if(self.componenetType=='script'):
            return self._createScript()
        if(self.componenetType=='container'):
            return self._createContainer()
        
    def _initializeForm(self, options):
        self.length = 0
        self.formFields = {}
        if('form_fields' in options):
            self.length = len(options['form_fields'])
            self.formFields = options['form_fields'][0:self.length]
        self.formClass = ''
        self.method = ''
        self.destination = ''
        if('form_class' in options):
            self.formClass = options['form_class']
        if('method' in options):
            self.method = options['method']
        if('action' in options):
            self.destination = options['action']
        self.labelClasses = {}
        for i in range(0,self.length):
            self.labelClasses[str(i)] = 'form-label'
        if('label_classes' in options):
            for (key,labelClass) in options['label_classes'].items():
                print(self.labelClasses[key])
                self.labelClasses[key] = labelClass
        self.inputClasses = {}
        for i in range(0,self.length):
            self.inputClasses[str(i)] = 'form-control'
        if('input_classes' in options):
            for key,inputClass in options['input_classes'].items():
                self.inputClasses[key] = inputClass
    
    def _createForm(self,request):
        element = '<form id="form" method=' + "'"+self.method+ "'" + ' action=' + "'" +self.destination+ "'" + ' class=' + "'"+ self.formClass+ "'"+'> '
        element += '<input name="csrfmiddlewaretoken" value='+ csrf.get_token(request) + ' type="hidden" />'
        for i in range(0,self.length):
            if('label' in self.formFields[i] and 'input_props' in self.formFields[i]):
                element += "<label class =" +self.labelClasses[str(i)] +" for ='" +  self.formFields[i]['label'] + ' id=' + self.formFields[i]['label'] + "_label" + "' >"+self.formFields[i]['label']+"</label>"
                fieldType = 'input'
                if 'field_type' in self.formFields[i]:
                    fieldType = self.formFields[i]["field_type"]
                element += '<'+fieldType+ ' class ='+ self.inputClasses[str(i)] +' id=' +"'" + self.formFields[i]['label']  +"_input"+ "'"+' style = "display:block;"'
                for (key,value) in self.formFields[i]['input_props'].items():
                    element += " "+ key+'='+'"'+value+'"'
                element += 'required >'
                if fieldType in ['select','datalist']:
                    if 'select_options' in self.formFields[i]:
                        for option in self.formFields[i]['select_options']:
                            element += '<option value=' +'"'+ option +'"'+'>' +option+'</option>'
                element += '</'+fieldType+'>'
        element += ' <input id = "submit" value="Submit" style = "display:block;margin-top:10px;" class = "btn btn-dark" type="submit">' 
        element += '</form>'
        return element
    
    def _initializeTable(self, options):
        self.tableClass = 'table'
        if ('table_class' in options):
            self.tableClass = options['table_class']
        self.tableHeader = []
        if ('table_header' in options):
            self.tableHeader = options['table_header'][:]
        self.tableRows = []
        if ('table_rows' in options):
            self.tableRows = options['table_rows'][:]
    
    def _createTable(self):
        element = '<table' + ' class=' + self.tableClass+'>'
        element += '<thead>'
        element += '<tr>'
        for field in self.tableHeader:
            element += " "+ '<th>'+ field +'</th>'
        element += '</tr>'
        element += '</thead>'
        
        for field in self.tableRows:
            element += '<tr>'
            for column in field:
                element += " "+ '<td>'+ column +'</td>'
            element += '</tr>'
        element += '</table>'

        return element
    
    def _initializeLink(self,options):
        self.linkClass = ''
        if('class' in options):
            self.linkClass = options['class']
        self.url = ''
        if('url' in options):
            self.url = options['url']
        self.target = ''
        if('target' in options):
            self.target = options['target']
        self.text = ''
        if('text' in options):
            self.text = options['text']
    
    def _createLink(self):
        element = '<a ' + 'class='+  '"' +self.linkClass + '"' + ' href=' + self.url + ' target=' + self.target + '>'+ self.text + '</a>'
        return element
    
    def _initializeScript(self,options):
        if('script' in options):
            self.script = options['script']
    def _createScript(self):
        return '<script>'+self.script+'</script>'
    def _initializeContainer(self,options):
        self.containerClass = ''
        if('class' in options):
            self.containerClass = options['class']
        self.type = ''
        if('type' in options):
            self.type = options['type']
        self.content = ''
        if('content' in options):
            self.content = options['content']
    def _createContainer(self):
        element = '<'+self.type+ ' class='+  '"' +self.containerClass + '"'+ '>'+ self.content + '</'+self.type+'>'
        return element