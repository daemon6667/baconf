#/usr/bin/env python

from resourcesconf import DefResources

def MatchResTypeHtmlType(res_type):
    result = None
    typ = res_type.lower()
    if typ in [ "int", "list", "integer", "fsize", "duration", "ipaddr", "ipaddextra", "enum", "string", ]:
       result = "text"
    elif typ in [ "bool", ]:
       result = "checkbox"
    elif typ in [ "password", ]:
       result = "password"
    return result

def MatchResTypeBottleType(res_type):
    result = None
    typ = res_type.lower()
    if   typ in [ "int", "integer", "fsize", "duration", ]: result = "int"
    elif typ in [ "ipaddr", "ipaddrextra", "string", ]: result = "text"
    elif typ in [ "enum", ]: result = "enum"
    elif typ in [ "list", ]: result = "list"
    elif typ in [ "bool", ]: result = "checkbox"
    elif typ in [ "password", ]: result = "password"
    else:
        result = "text"
        print("Type is not recognized: %s" % res_type)
    return result

class HtmlFormAddResource:
    m_defresources = None
    def __init__(self, def_resources):
        self.m_defresources = def_resources

    def makeFieldsCode(self, language, section):
        attrs = self.m_defresources.section(section)
        result_required_fields = ""
        result_optional_fields = ""
        result_field_name = ""
        def add_field_block(lang, attr, name, f_type):
            result = ""
            if lang == 'html':
                result_html = """
                <div class="w2ui-field">
                    <div><label>%s<input name="%s" type="%s" size="100" /></label></div>
                </div>""" % (attr, name, MatchResTypeHtmlType(f_type))
                result = result_html
            elif lang == 'javascript':
                result_js = """
                    { name: '%s', type: '%s'%s%s }, """ % (
                    name,
                    MatchResTypeBottleType(f_type),
                    ', required: true' if ('required' in props and props['required'].lower() == 'true') else '',
                    ", options: { items: %s }" % (str(self.m_defresources.list_possiblevalues(section, attr)    )) if (props['type'].lower() in ['enum', 'list']) else ''
                )
                result = result_js
            return result
 
        for attr in attrs:
            props = self.m_defresources.attr_properties(section, attr)
            name = attr.replace(' ', '').lower()
            if 'required' in props and props['required'].lower() in ['true', ]:
                field = add_field_block(language, attr, name, props['type'])
                if name.lower() == 'name':
                    result_field_name = field
                else:
                    result_required_fields += field
            else:
                result_optional_fields += add_field_block(language, attr, name, props['type'])
        result = ""
        if language == 'html':
            result = """
            <div class="w2ui-page page-0">
            <div class="w2ui-field">
                 <div><label>Namespace<input name="specific_namespace" type="text" size="100" /></label></div>
            </div>
            <div class="w2ui-field">
                 <div><label>Enabled<input name="specific_enabled" type="checkbox" size="100" /></label></div>
            </div>
			<hr />
            %s%s
            </div>
            <div class="w2ui-page page-1">%s
            </div>
            """ % (result_field_name, result_required_fields, result_optional_fields)
        elif language == "javascript":
            result = "" + result_field_name + result_required_fields + result_optional_fields
        return result

    def makeJS(self, section, namespaces):
        return """
        function make_form(form_name) {
            $('#formadd').w2form({
                name: '' + form_name,
                header: 'Adding new item of %s resource type',
                url:  '/htmladd/%s/save',
                formURL: '/htmladd/%s/html',
                fields: [
                    { name: 'specific_namespace', type: 'list', required: true, options: { items: %s } },
                    { name: 'specific_enabled', type: 'bool', required: true, },
                   %s 
                ],
                tabs: [
                    { id: 'tab1', caption: 'Mandatory options'},
                    { id: 'tab2', caption: 'Optional features'},
                ],
                actions: {
                    reset: function() {
                        this.clear();
                    },
                    save: function() {
                        this.save();
                    }
                },
                postData: {
                    restype: '%s'
                }
            });
/*
			$(function() {
				$.get('/get/namespaces', function(data) {
					$('input[type=list]').w2field('specific_namespace', { items: JSON.parse(data) });
				})
			}); 
*/
        };
        """ % (section, section, section, namespaces, self.makeFieldsCode('javascript', section), section)

    def makeHtml(self, section):
        return """
        <div id="form" style="width: 100%%; height: 100%%;">
            %s
            <div class="w2ui-buttons">
                <button class="btn" name="reset">Reset</button>
                <button class="btn btn-green" name="save">Save</button>
            </div>
        </div>
        """ % (self.makeFieldsCode('html', section))

if __name__ == "__main__":
    h = HtmlFormAddResource(DefResources('resources.def'))
    #print(h.makeFieldsCode('javascript', 'Device'))
    #print(h.makeJS('Device'))
    print(h.makeHtml('Device'))
    pass
