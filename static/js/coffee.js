var cookbook_list;
cookbook_list = {};
cookbook_list.vm = function(){
  var vm;
  vm = {};
  vm.init = function(){
    vm.list = [];
  };
  vm.cookbooks = m.request({
    method: 'GET',
    url: '/plugin/coffee/cookbooks'
  });
  return vm;
}();
cookbook_list.view = function(ctrl){
  var generate_item, name, metadata;
  generate_item = function(name){
    return m("div.ui.item", [m("div.content", [m("a.header", name)])]);
  };
  return m("div", (function(){
    var ref$, results$ = [];
    for (name in ref$ = cookbook_list.vm.cookbooks()) {
      metadata = ref$[name];
      results$.push(generate_item(name));
    }
    return results$;
  }()));
};
cookbook_list.controller = function(){
  cookbook_list.vm.init();
};
m.module(document.getElementById("sidebar"), cookbook_list);