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

        if "content" in metadata
            @content = metadata["content"]
        else
            @content = ""

module.exports = Cookbook
