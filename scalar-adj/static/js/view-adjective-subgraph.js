var adj_list, size, links, path, circle, text, force, container;


$( document ).ready(function() {
  adj_list = $(".adj_list").attr("id").replace(", ", ".");
  size = $("#size").text();
  render();

  $("#goButton").click(function() {
    s = $("#newAdjSrc").val().split(', ').join(',');
    adjList = s.split(',').join('.');
    window.location.href = '/view-adjective-subgraph/' + adjList;
  })

});

// ["pineapple", "owjeg", "aoie"] will return true for "pineapple", false for "apple"
function arrayContainsFullWord(arr, word) {
  for (var i = 0; i < arr.length; i++) {
    if (arr[i] === word) {
      return true;
    }
  }
  return false;
}

function render() {
  
  links = [];
  // get cycle words for this graph
  $.getJSON( '/get/adjective-subgraph/' + adj_list, function( data ) {
    $.each( data, function( key, val ) {
      var info = val;
      var source = info.source;
      var target = info.target;
      var relationshipWord = info.relationshipWord;
      var color = "gray";
      var temp = {source: source, target: target, type: "suit", color: color, relationshipWord: relationshipWord}
      
      links.push(temp)
    });

    draw();


  }).error(function() { $("#error").html("There were no edges stemming from \"" + adj_list + "\"") });

  
}

function draw() {
  if (links.size == 0) {
    $("#error").html("There were no edges stemming from \"" + adj_list + "\"")
    return
  }
  var nodes = {};
  var spaceId = "#graphSpace"
  // Compute the distinct nodes from the links.
  links.forEach(function(link) {
    var sColor = "#2F4F4F";
    var tColor = "#2F4F4F";

    link.source = nodes[link.source] || (nodes[link.source] = {name: link.source, color: sColor});
    link.target = nodes[link.target] || (nodes[link.target] = {name: link.target, color: tColor});
  });

  margin = {top: -5, right: -5, bottom: -5, left: -5};
  width = $(".graphSpace").width() - margin.left - margin.right;
  height = $(".graphSpace").height() - margin.top - margin.bottom;

  var force = d3.layout.force()
      .charge(-1200)
      .linkDistance(240)
      .size([width + margin.left + margin.right, height + margin.top + margin.bottom])

  var zoom = d3.behavior.zoom()
      .scaleExtent([-0.1, 10])
      .on("zoom", zoomed);

  var drag = d3.behavior.drag()
      .origin(function(d) { return d; })
      .on("dragstart", dragstarted)
      .on("drag", dragged)
      .on("dragend", dragended);

  var svg = d3.select(spaceId).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.right + ")")
    .call(zoom)
    .on("contextmenu", function(data, index) {
        event.preventDefault();
      });


  var rect = svg.append("rect")
  .attr("width", width)
  .attr("height", height)
  .style("fill", "none")
  .style("pointer-events", "all");

  var container = svg.append("g");

  force
    .nodes(d3.values(nodes))
    .links(links)
    .on("tick", tick)
    .start();

  // Per-type markers, as they don't inherit styles.
  var markers = container.append("g").selectAll("marker")
      .data(["suit"])
    .enter().append("marker")
      .attr("id", function(d) { return d; })
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 12)
      .attr("refY", -1.2)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
    .append("path")
      .attr("d", "M0,-5L10,0L0,5");

 var path = container.append("g").selectAll("path")
      .data(force.links())
    .enter().append("path")
      .attr("class", function(d) { return "link " + d.type; })
      .attr("marker-end", function(d) { return "url(#" + d.type + ")"; })
      .style("stroke", function(d) { return d.color; })
      .on("mouseover", function(d){if (!dragInitiated) {return tooltip.style("visibility", "visible").html(
        "| <span style='color: red'>" + d.relationshipWord + "</span> <span style='color: blue'>" + d.source.name + "</span> | -> " + "| <span style='color: darkgreen'>" + 
         d.target.name + "</span> |")} 
      })
      .on("mousemove", function(){return tooltip.style("top",
          (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");});



 var dragInitiated = false;
  var tooltip = d3.select("body")
    .append("div")
    .attr("class", "well")
    .attr("id", "tooltip")
    .style({"position": "absolute", "z-index": "10", "visibility": "hidden", "background-color":"white", "padding": "10px"})

  var circle = container.append("g").selectAll("circle")
      .data(force.nodes())
      .enter().append("g")
      .attr("class", "circle")
                        .attr("cx", function(d) { return d.x; })
                        .attr("cy", function(d) { return d.y; })
                        .call(drag)

      .on("contextmenu", function(data, index) {
        event.preventDefault();
        // similar behavior as clicking on a link
        window.location.href = '/view-adjectives/' + data.name + '/' + $("#size").text();
      })
      .append("circle")
      .attr("r", 6)
      .style("fill", function(d) { return d.color; })
      .on("mouseover", function(d){if (!dragInitiated) {return tooltip.style("visibility", "visible").text(d.name)} })
      .on("mousemove", function(){return tooltip.style("top",
          (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");});

  var text = container.append("g").selectAll("text")
      .data(force.nodes())
    .enter().append("text")
      .attr("x", 8)
      .attr("y", ".31em")
      .text(function(d) {return d.name;});

  // Use elliptical arc path segments to doubly-encode directionality.
  function tick() {
    path.attr("d", linkArc);
    circle.attr("transform", transform);
    text.attr("transform", transform);
  }

  function linkArc(d) {
    var dx = d.target.x - d.source.x,
        dy = d.target.y - d.source.y,
        dr = Math.sqrt(dx * dx + dy * dy);
    return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
  }

  function transform(d) {
    return "translate(" + d.x + "," + d.y + ")";
  }   

  function zoomed() {
    container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  }



  function dragstarted(d) {
    // initiate on left mouse button only
    if (d3.event.sourceEvent.which == 1) {
      dragInitiated = true;

      d3.event.sourceEvent.stopPropagation();
      
      d3.select(this).classed("dragging", true);
      force.start();
    } 
  }


  function dragged(d) {
    if (dragInitiated) {
      d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
    }
    
  }

  function dragended(d) {
    if (d3.event.sourceEvent.which == 1) {
      d3.select(this).classed("dragging", false);
      dragInitiated = false;
    }
  }

}
