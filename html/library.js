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

