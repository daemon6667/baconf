function load_mainboard() {
    var pstyle = 'background-color: #F5F6F7; border: 1px solid #dfdfdf; padding: 5px;';
    $("#mainworkplace").w2layout({
        name: 'mainworkplace',
        panels: [
            { type: 'left', size: 200, resizable: true, style: pstyle, content: 'left' },
            { type: 'main', style: pstyle, content: 'main', 
                toolbar: [
                    { id: 1, type: 'button', caption: 'Test button' },
                ],
            },
            { type: 'top', size: 35, style: pstyle, content: 'Stand by panel' },
            { type: 'right', size: 350, resizable: true, style: pstyle, content: '' },
        ]
    }); 
    w2ui['mainworkplace'].content('left', w2ui['sidebar']);
    w2ui['mainworkplace'].toggle('right', window.instant);
};

function load_list_resources() {
	$('#list_resources').w2grid({
		name: 'list_resources',
		header: 'List of resources',
		url: '/resources',
		show: {
            header: true,
			toolbar: true,
			footer: true,
			toolbarAdd: false,
			toolbarDelete: true,
		},
        toolbar: {
            items: [
                { type: 'break' },
                { type: 'button', id: 'show-item', caption: 'Show selected item', img: 'icon-folder' },
                { type: 'button', id: 'show-namespace-items', caption: 'Show all items in the NS', img: 'icon-folder' }
            ],
        },
        /*
        menu: [
            { id: 1, text: 'Show item', icon: 'fa-star' },
        ],
        */
		columns: [
			{ field: 'recid', caption: 'ID', size: '30px', sortable: true, attr: 'align=center' },
			{ field: 'namespace', caption: 'Namespace', size: '80px', sortable: true, attr: 'align=center' },			
			{ field: 'restype',  caption: 'Resource Type', size: '100px', sortable: true },
			{ field: 'name',  caption: 'Name', size: '200px', sortable: true },
			{ field: 'enabled', caption: 'Enabled', size: '75px', sortable: true, attr: 'align=center' },
		],
		// sortData: [{field: 'type', direction: 'ASC'}, {field: 'name', director: 'ASC'}],
	});
	w2ui['mainworkplace'].content('main', w2ui['list_resources'])
};

function load_sidebar() {
	$.get('/def/resource', function(data) {
		var j_data = JSON.parse(data);
		var resources = [];
		if (j_data.success == true)
			var i = 0;
			j_data.data.sort();
			for (i = 0; i < j_data.data.length; i++)
				resources[resources.length] = { id: 'newitem_' + j_data.data[i], text: '' + (i+1) + '. ' + j_data.data[i], img: 'icon-page' }
		console.log(j_data);
		console.log(resources);
		$('#sidebar').w2sidebar({
			name: 'sidebar',
			nodes: [
				{ id: 'list_resources', text: 'Defined resources', img: 'icon-page', expanded: true },
				{ id: 'level-1-resources', text: 'Adding resources', img: 'icon-folder', expanded: false, nodes: resources },
			],
			onClick: function(event) {
				console.log("You pressed: " + event.target);
				if (event.target == 'list_resources') {
					load_list_resources();		
				} else if (event.target.substring(0, 8) == 'newitem_') {
					var res_name = event.target.substring(8);
					console.log("Selected resource type is: " + res_name);					
					formadd_resource(res_name);
				}
			}
		})
		w2ui['mainworkplace'].content('left', w2ui['sidebar']);
	});
};

function formadd_resource(resource_type) {
	$.getScript('/htmladd/' + resource_type + '/js')
		.done(function() { 
			console.log( "Loading successed" );
			var form_name = 'form_' + resource_type;
	//		if (w2ui.checkName(w2form[form_name], 'w2form') == true) 
	//			$().w2destroy(form_name);
			make_form(form_name); 
			w2ui['mainworkplace'].content('main', w2ui[form_name]);
		});
};

