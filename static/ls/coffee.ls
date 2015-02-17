cookbook_list = {}

Cookbooks = (raw_data) ->
    for name, metadata of raw_data
        new Cookbook(name, metadata)

class Cookbook 
    format_date: (date_time) ->
        dd = new Date(date_time * 1000)
        dd.getFullYear! + '/' + (dd.getMonth! + 1) + "/" + dd.getDate! + " " +
            dd.getHours! + ":" + dd.getMinutes! + ":" + dd.getSeconds!

    (name, metadata) ->
        @name = name
        @created_date = @format_date(metadata['date'])
        @estimated_time = metadata["analysis"]["estimatedPrintTime"]
        @volume = metadata["analysis"]["filament"]["tool0"]["volume"]
        @length = metadata["analysis"]["filament"]["tool0"]["length"]

cookbook_list.vm = do ->
    vm = {}

    vm.init = ! ->
        vm.list = []

    vm.cookbooks = m.request {method: 'GET', url: '/plugin/coffee/cookbooks', type: Cookbooks}

    vm

cookbook_list.view = (ctrl) ->
    generate_item = (cookbook) ->
        m "div.ui.item", [
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

    m "div.ui.items", for cookbook in cookbook_list.vm.cookbooks!
        generate_item(cookbook)

cookbook_list.controller = ! ->
    cookbook_list.vm.init!

m.module (document.getElementById "sidebar"), cookbook_list
