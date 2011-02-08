var vis = new pv.Panel().canvas('fig')
    .width(300)
    .height(300)
  .add(pv.Line)
    .data(data)
    .left(function() {return this.index * 30;})
    .bottom(function(d) {return d * 250;});

vis.root.render();
