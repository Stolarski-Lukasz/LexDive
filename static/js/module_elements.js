export function create_element(options) {

  //  specifying named parameters
  ///////////////////////////////
  var opts = {};
  opts.tag = options.tag || "div";
  opts.className = options.className || undefined;
  opts.id = options.id || undefined;
  opts.innerText = options.innerText || undefined;
  // style
  opts.style_margin = options.style_margin || undefined;
  opts.style_width = options.style_width || undefined;
  // other
  opts.rows = options.rows || undefined;
  opts.role = options.role || undefined;
  // appending
  opts.parent_id = options.parent_id || undefined;

  // body of the function
  ///////////////////////
  var new_element = document.createElement(opts.tag);
  if (opts.className != undefined) {
    new_element.className = opts.className;
  }
  if (opts.id != undefined) {
    new_element.id = opts.id;
  }
  if (opts.innerText != undefined) {
    new_element.innerText = opts.innerText;
  }
  if (opts.style_margin != undefined) {
    new_element.style.margin = opts.style_margin;
  }
  if (opts.style_width != undefined) {
    new_element.style.width = opts.style_margin;
  }
  if (opts.rows != undefined) {
    new_element.rows = opts.rows;
  }
  if (opts.rows != undefined) {
    new_element.role = opts.role;
  }
  if (opts.parent_id != undefined) {
    var parent = document.getElementById(opts.parent_id);
    parent.appendChild(new_element);
  }

  return new_element
};



export function remove_element(id) {
  var element_for_removal = document.getElementById(id);
  if (typeof (element_for_removal) != 'undefined' && element_for_removal != null) {
    element_for_removal.parentNode.removeChild(element_for_removal);
  }
};



export function remove_children(id) {
  var parent_element = document.getElementById(id);
  if (typeof (parent_element) != 'undefined' && parent_element != null) {
    parent_element.innerHTML = "";
  }
};

