cookbook_list = {}

cookbook_list.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.list = []

    vm.cookbooks = m.request {method: 'GET', url: '/plugin/coffee/cookbooks'}
    vm

cookbook_list.view = (ctrl) ->

    generate_item = (name) ->
        m "li", [
            m "a.list-group-item", [
                m "h4.list-group-item-heading" name
            ]
        ]

    m "ul.nav.list-group",
        for name, metadata of cookbook_list.vm.cookbooks!
            generate_item(name)

cookbook_list.controller = ! ->
    cookbook_list.vm.init!

m.module (document.getElementById "sidebar"), cookbook_list 
