var cookbook_list, Cookbooks, Cookbook;
cookbook_list = {};
Cookbooks = function(raw_data){
  var name, metadata, results$ = [];
  for (name in raw_data) {
    metadata = raw_data[name];
    results$.push(new Cookbook(name, metadata));
  }
  return results$;
};
Cookbook = (function(){
  Cookbook.displayName = 'Cookbook';
  var prototype = Cookbook.prototype, constructor = Cookbook;
  prototype.format_date = function(date_time){
    var dd;
    dd = new Date(date_time * 1000);
    return dd.getFullYear() + '/' + (dd.getMonth() + 1) + "/" + dd.getDate() + " " + dd.getHours() + ":" + dd.getMinutes() + ":" + dd.getSeconds();
  };
  function Cookbook(name, metadata){
    this.name = name;
    this.created_date = this.format_date(metadata['date']);
    this.estimated_time = metadata["analysis"]["estimatedPrintTime"];
    this.volume = metadata["analysis"]["filament"]["tool0"]["volume"];
    this.length = metadata["analysis"]["filament"]["tool0"]["length"];
  }
  return Cookbook;
}());
cookbook_list.vm = function(){
  var vm;
  vm = {};
  vm.init = function(){
    vm.list = [];
  };
  vm.cookbooks = m.request({
    method: 'GET',
    url: '/plugin/coffee/cookbooks',
    type: Cookbooks
  });
  return vm;
}();
cookbook_list.view = function(ctrl){
  var generate_item, cookbook;
  generate_item = function(cookbook){
    return m("div.ui.item", [m("div.content", [m("a.header", cookbook.name), m("div.meta", cookbook.created_date), m("div.description", [m("div", cookbook.estimated_time), m("div", cookbook.volume), m("div", cookbook.length)])])]);
  };
  return m("div.ui.items", (function(){
    var i$, ref$, len$, results$ = [];
    for (i$ = 0, len$ = (ref$ = cookbook_list.vm.cookbooks()).length; i$ < len$; ++i$) {
      cookbook = ref$[i$];
      results$.push(generate_item(cookbook));
    }
    return results$;
  }()));
};
cookbook_list.controller = function(){
  cookbook_list.vm.init();
};
m.module(document.getElementById("sidebar"), cookbook_list);