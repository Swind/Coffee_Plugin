require! {
    "components/cookbook.js": Cookbook 
}

cookbook_content = {}

# ================================================================================
#
#   View 
#
# ================================================================================
cookbook_content.view = (ctrl) ->
    selected_cookbook = cookbook_content.vm.selected_cookbook!
    (m "h2.ui.dividing.header", [selected_cookbook.name,
        (m "div.ui.segment", [selected_cookbook.content])
    ])

# ================================================================================
#
#   View Model 
#
# ================================================================================
cookbook_content.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.selected_cookbook = m.prop {}

    vm

cookbook_content.controller = ! ->
    cookbook_content.vm.init!

    @name = m.route.param("name");
    @get_selected_cookbook = (name) ->
        m.request (
            {
                method: 'GET',
                url: '/plugin/coffee/cookbooks/' + name
            }
        )
        .then((metadata) -> new Cookbook(name, metadata))
        .then(cookbook_content.vm.selected_cookbook)

    if @name != void 
        @get_selected_cookbook(@name)

module.exports = cookbook_content
