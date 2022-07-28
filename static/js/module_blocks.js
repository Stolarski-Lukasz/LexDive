// importing modules
import {
  create_element,
  remove_element,
  remove_children
} from "./module_elements.js"



export function delete_ld_results() {
  remove_element("warning")
  remove_element("ld_results_parent");
  remove_children("table_parent2");
  remove_element("ld_results_horizontal_line")
};


export function create_separator(parent_id) {
  var separator_div = document.createElement("div");
  separator_div.className = "col-xs-12";
  separator_div.style.height = "1em";
  var parent = document.getElementById(parent_id);
  parent.appendChild(separator_div);
};


export function create_table_skeleton(table_parent_id, table_id) {
  create_element({ tag: "div", className: "card text-center mb-4", id: "table_container_div", parent_id: table_parent_id });
  create_element({ tag: "div", className: "card-header", id: "card_header_div", innerText: "Subsamples List", parent_id: "table_container_div" });
  create_element({ tag: "i", className: "fas fa-table mr-1", id: "i_something", parent_id: "card_header_div" });
  create_element({ tag: "div", className: "card-body text-center", id: "card_body_div", parent_id: "table_container_div" });
  create_element({ tag: "div", className: "table-responsive", id: "table_responsive_div", parent_id: "card_body_div" });
  create_element({ tag: "table", className: "table-sm table-bordered", id: table_id, style_width: "100%", parent_id: "table_responsive_div" });

}