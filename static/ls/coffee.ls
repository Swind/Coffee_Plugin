cookbook_list = {}

cookbook_list.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.list = []

    vm.cookbooks = m.request {method: 'GET', url: '/plugin/coffee/cookbooks'}
    vm

cookbook_list.view = (ctrl) ->

    generate_item = (name) ->
        m "div.ui.item", [
            m "div.content", [
                m "a.header" name
            ]
        ]

    m "div", for name, metadata of cookbook_list.vm.cookbooks!
        generate_item(name)

cookbook_list.controller = ! ->
    cookbook_list.vm.init!

m.module (document.getElementById "sidebar"), cookbook_list 
