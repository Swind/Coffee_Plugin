require! {
    "components/cookbook_list.js": cookbook_list
    "components/cookbook_content.js": cookbook_content
}

m.module (document.getElementById "sidebar"), cookbook_list

m.route (document.getElementById "main"), "/cookbook_content", {
        "/cookbook_content": cookbook_content 
        "/cookbook_content/:name": cookbook_content 
}
