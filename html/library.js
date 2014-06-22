function load_mainboard() {
    var pstyle = 'background-color: #F5F6F7; border: 1px solid #dfdfdf; padding: 5px;';
    $("#mainworkplace").w2layout({
        name: 'mainworkplace',
        panels: [
            { type: 'left', size: 200, resizable: true, style: pstyle, content: 'left' },
            { type: 'main', style: pstyle, content: 'main' },
            { type: 'top', size: 35, style: pstyle, content: 'PUT HERE NAME OF A CURRENT PAC FILE' },
            { type: 'right', size: 350, resizable: true, style: pstyle, content: '' },
        ]
    }); 
    w2ui['mainworkplace'].content('left', w2ui['sidebar']);
    w2ui['mainworkplace'].toggle('right', window.instant);
    w2ui.sidebar.hide('level-1-proxies', 'level-1-changes-commit', 'level-1-rule-add', 'level-1-rules', 'level-1-pacfile-show', 'level-1-merge-pacfile', 'level-1-pacfile-show-updated');
};

function load_sidebar() {
    $('#sidebar').w2sidebar({
        name: 'sidebar',
        nodes: [
            { id: 'level-1', text: 'Choose action', img: 'icon-folder', expanded: true, group: true,
                nodes: [
                    { id: 'level-1-resources', text: 'Resources', pac: 'fs-start' },
                    { id: 'level-1-rules', text: 'List rules', pac: 'fa-home' },
                    { id: 'level-1-rule-add', text: 'Add a new rule', pac: 'fa-star' },
                    { id: 'level-1-pacfile-show', text: 'Show pac', pac: 'fa-star' },
                    { id: 'level-1-pacfile-show-updated', text: 'Show updated pac', pac: 'fa-star' },
                    { id: 'level-1-changes-commit', text: 'Commit changes', pac: 'fa-start-empty' },
                    { id: 'level-1-merge-pacfile', text: 'Merge Data', pac: 'fa-star' },
//                    { id: 'level-1-proxies', text: 'List proxies', pac: 'fa-star-empty' },
                ],
            }
        ],
        onClick: function(event) {
            console.log("Target: " + event.target);
            if (event.target == 'level-1-resources') {
                load_listpacfiles();
                w2ui['mainworkplace'].content('main', w2ui['list_pacfiles'])
            } else if (event.target == 'level-1-rules') {
                w2ui['mainworkplace'].content('main', w2ui['list_rules'])
                //w2ui['mainworkplace'].content('main', w2ui.list_rules);
            } else if (event.target == 'level-1-rule-add') {
                form_rule_edit();
                // some code and maybe no
            } else if (event.target == 'level-1-pacfile-show-updated') {
                $.get('/json/pacfile/' + selected_pacfile + '/updatedfile', function (data) {
                    w2ui['mainworkplace'].html('main', data.content); 
                })
            } else if (event.target == 'level-1-pacfile-show') {
                $.get('/json/pacfile/' + selected_pacfile + '/show', function (data) {
                    w2ui['mainworkplace'].html('main', data.content); 
                })
            } else if (event.target == 'level-1-changes-commit') {
                load_listupdates();
            } else {
                w2ui['mainworkplace'].html('main', 'Other link was pressed');
            } 
        }
    })
};

function load_listrules(pacfile) {
    console.log("Selected pacfile is " + selected_pacfile);
    $('#list_rules').w2grid({
        name: 'list_rules',
        header: 'The list of defined rules in the PAC file',
        url: '/json/pacfile/' + pacfile + '/rules',
        //url: '/json/pacfile/' + selected_pacfile + '/rules',
        show: {
            header: true,
            lineNumbers: true,
            toolbar: true,
            toolbarAdd: false,
            toolbarEdit: false,
            toolbarDelete: true,
            multiSelect: true,
            footer: true,
            selectColumn: true,
        },
        multiSelect: false, 
        columns: [
            { field: 'id', caption: 'ID', size: '10%', sortable: true, },
            { field: 'function', caption: 'Compare function', size: '25%', sortable: true, },
            { field: 'userdata', caption: 'User data', size: '40%', sortable: true, },
            { field: 'proxy', caption: 'Proxy', size: '25%', sortable: true, },
        ],
    })
}
