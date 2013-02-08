#!/usr/bin/env python
#
# (c) 2013 Joost Yervante Damad <joost@damad.be>
# License: GPL


import PyV8
import os.path

class Global(PyV8.JSClass):

    def __init__(self):
      self.path = ""

    def require(self, arg):
      content = ""
      with open(self.path+arg+".js") as file:
        file_content = file.read()
      result = None
      try:
        store_path = self.path
        self.path = self.path + os.path.dirname(arg) + "/"
        result = PyV8.JSContext.current.eval(file_content)
      finally:
        self.path = store_path
      return result

def make_js_from_coffee(coffee_script_code):
  with PyV8.JSContext(Global()) as ctxt:
    js_make_js_from_coffee = ctxt.eval("""
(function (coffee_code) {
  CoffeeScript = require('coffee-script/coffee-script');
  js_code = CoffeeScript.compile(coffee_code, null);
  return js_code;
})
""")
    return js_make_js_from_coffee(coffee_script_code)

def eval_js_footprint(js):
  with PyV8.JSContext() as ctxt:
      return PyV8.convert(ctxt.eval(js+"; shapes();"))

def eval_coffee_footprint(coffee):
  ground = ""
  with open("ground.coffee") as f: ground = f.read()
  js = make_js_from_coffee(ground + "\n" + coffee + "\nreturn shapes()\n")
  with PyV8.JSContext() as ctxt:
      return PyV8.convert(ctxt.eval(js))

js_example = """
function shapes() {
  var xs = [-2, -1, 0, 1, 2];
  var rect1 = { shape: 'rect', dx: 0.8, dy: 2, ro: 50 };
  function xmod(x) {
    var b = Object();
    b.shape = rect1.shape;
    b.dx = rect1.dx; 
    b.dy = rect1.dy;
    b.ro = rect1.ro;
    b.x = x; return b;
  }
  return xs.map(xmod);
}
"""

coffee_example = """
shapes = () ->
  rect1 = 
    shape: 'rect'
    dx: 0.8
    dy: 2
    ro: 50
  
  range rect1, 'x', [-2, -1, 0, 1, 2]
"""
