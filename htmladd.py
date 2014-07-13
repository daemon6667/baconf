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
    return result

class HtmlFormAddResource:
    m_defresources = None
    def __init__(self, def_resources):
        self.m_defresources = def_resources

    def makeJS(self, section, fields):
        result = """
        function make_formadd() {
            $('#form').w2form({
                name: 'form',
                url:  'htmladd/save',
                formURL: 'htmladd/%s/html',
                fields: [
                   %s 
                ],
                actions: {
                    reset: function() {
                        this.clear();
                    },
                    save: function() {
                        this.save();
                    }
                }
            })
        };
        """ % (section, fields)
        return result

    def makeHtml(self, section):
        result_html = """
        <div id="form" style="width: 100%;">
            <div class="w2ui-page page-0">
        """
        jsfields = ""
        attrs = self.m_defresources.section(section)
        for attr in attrs:
            props = self.m_defresources.attr_properties(section, attr)
            name = attr.replace(' ', '').lower()
            result_html += """
                <div class="w2ui-field">
                    <label>%s</label>
                    <div>
                        <input name="%s" type="%s" size="60" />
                    </div>
                </div>
            """ % (attr, name, MatchResTypeHtmlType(props['type']))
                 
            jsfields += """
                    { name: '%s', type: '%s'%s%s }, """ % (
                        name, 
                        MatchResTypeBottleType(props['type']),
                        ', required: true' if ('required' in props and props['required'].lower() == 'true') else '',
                        ", options: { url: '/get/resource/%s/%s/values', items: %s }" % (section, name, str(self.m_defresources.list_possiblevalues(section, attr))) if (props['type'].lower() in ['enum', 'list']) else ''
                    )
        result_html += """
            </div>
            <div class="w2ui-buttons">
                <button class="btn" name="reset">Reset</button>
                <botton class="btn" name="save">Save</button>
            </div>
        </div>
        </div>
        """
        result_js = """
        %s
        """ % (self.makeJS(section, jsfields))
        return (result_html, result_js)

if __name__ == "__main__":
    h = HtmlFormAddResource(DefResources('resources.def'))
    print(h.makeHtml('Device')[1])
    pass
