function load_mainboard() {
    var pstyle = 'background-color: #F5F6F7; border: 1px solid #dfdfdf; padding: 5px;';
    $("#mainworkplace").w2layout({
        name: 'mainworkplace',
        panels: [
            { type: 'left', size: 200, resizable: true, style: pstyle, content: 'left' },
            { type: 'main', style: pstyle, content: 'main' },
            { type: 'top', size: 35, style: pstyle, content: 'Stand by panel' },
            { type: 'right', size: 350, resizable: true, style: pstyle, content: '' },
        ]
    }); 
    w2ui['mainworkplace'].content('left', w2ui['sidebar']);
    w2ui['mainworkplace'].toggle('right', window.instant);
//    w2ui.sidebar.hide('level-1-proxies', 'level-1-changes-commit', 'level-1-rule-add', 'level-1-rules', 'level-1-pacfile-show', 'level-1-merge-pacfile', 'level-1-pacfile-show-updated');
};

function load_list_resources() {
	$('#list_resources').w2grid({
		name: 'list_resources',
		header: 'List of resources',
		show: {
			toolbar: true,
			footer: true,
			toolbarAdd: true,
			toolbarDelete: true,
		},
		columns: [
			{ field: 'recid', caption: 'ID', size: '30px', sortable: true, attr: 'align=center' },
			{ field: 'enabled', caption: 'Enabled', size: '75px', sortable: true, attr: 'align=center' },
			{ field: 'type',  caption: 'Resource Type', size: '250px', sortable: true },
			{ field: 'name',  caption: 'Name', size: '200px', sortable: true } 	
		],
		sortData: [{field: 'type', direction: 'ASC'}, {field: 'name', director: 'ASC'}],
		onAdd: {
			
		}
	});
};

function load_sidebar() {
    $('#sidebar').w2sidebar({
        name: 'sidebar',
        nodes: [
            { id: 'level-1', text: 'Choose action', img: 'icon-folder', expanded: true, group: true,
                nodes: [
                    { id: 'level-1-resources', text: 'Load', pac: 'fs-start' },
                    { id: 'level-1-add-device', text: 'new Device', pac: 'fa_device' },
                ],
            }
        ],
        onClick: function(event) {
            console.log("Target: " + event.target);
            if (event.target == 'level-1-resources') {
                load_list_resources();
                w2ui['mainworkplace'].content('main', w2ui['list_resources'])

            } else if (event.target == 'level-1-add-device') {
				formadd_resource('Device');
                //w2ui['mainworkplace'].content('main', w2ui['form'])
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

function formadd_resource(resource_type) {
	$('#list_resources').load('/htmladd/' + resource_type);
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
