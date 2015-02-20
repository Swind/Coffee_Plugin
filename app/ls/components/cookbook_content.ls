cookbook_content = {}

# ================================================================================
#
#   View 
#
# ================================================================================
cookbook_content.view = (ctrl) ->
    (m "h2.ui.dividing.header", [ctrl.vm.selected!.id,
        (m "div.ui.segment", [ctrl.vm.selected!.content])
    ])

# ================================================================================
#
#   View Model 
#
# ================================================================================
cookbook_content.controller = (vm) ->
    @vm = vm 
    this

module.exports = cookbook_content
