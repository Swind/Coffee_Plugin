require! {
    "components/cookbook.js": Cookbook 
}

cookbook_list = {}

# ================================================================================
#
#   View Model 
#
# ================================================================================
Cookbooks = (raw_data) ->
    for name, metadata of raw_data
        new Cookbook(name, metadata)

cookbook_list.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.cookbooks = m.request ({method: 'GET', url: '/plugin/coffee/cookbooks', type: Cookbooks})

    vm

# ================================================================================
#
#   View and Controller
#
# ================================================================================
cookbook_list.view = (ctrl) ->
    generate_item = (cookbook) ->
        m "a.ui.item", {id: "cookbook-item", href: "?/cookbook_content/" + cookbook.name},[
            (m "div.content", [
                (m "a.header" cookbook.name),
                (m "div.meta" cookbook.created_date),
                (m "div.description", [
                    (m "div" cookbook.estimated_time),
                    (m "div" cookbook.volume),
                    (m "div" cookbook.length)
                ])
            ])
        ]

    m "div.ui.items.divided", for cookbook in cookbook_list.vm.cookbooks!
        generate_item(cookbook)

cookbook_list.controller = ! ->
    cookbook_list.vm.init!

module.exports = cookbook_list
