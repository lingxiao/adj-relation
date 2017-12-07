var pos, size, dir_path, collapsedEdgesFile, collapsedVerticesFile,
  cyclePathsFile, cyclePhrasesFile, originalEdgesFile, originalVerticesFile,
  path, circle, text, force, container, original_links, collapsed_links, wordToAdjacents, cycle_word;

var viewing_original = true;

$( document ).ready(function() {
  
  pos = $("#pos").text();
  size = $("#size").text();

  $("#collapsedSpace").hide();
  $("#originalButton").hide();
  render_original();

  $("#originalButton").click(function() {
    $("#collapsedSpace").hide();
    $("#originalSpace").show();
    $("#originalButton").hide();
  });

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

function render_original() {
  original_links = [];
  // dictionary of words to the words that they touch in a cycle with a
  // forward directed edge
  // e.g {"transformations": ["reforms"]}
  wordToAdjacents = {};
  var cyclePhrases = [];


  // get cycle words for this graph
  $.get( '/get/cycle-phrases/' + pos + '/' + size, function( data ) {
    
    cyclePhrases = JSON.parse(data);


    // get cycle paths for this graph
    $.get( '/get/cycle-paths/' + pos + '/' + size, function( data ) {

      // store which cycle words touch for later
      if (data.length == 0) {
        return;
      }
      var paths = data.split("\n");
      var numPaths = 0;
      for (var i = 0; i < paths.length; i++) {
        numPaths++;
        var path = JSON.parse(paths[i]);
        $("#cycles").append("<li><b>" + numPaths + ".</b> " + path.join(", ") + "</li>");
        for (var j = 0; j < path.length; j++) {
          var p1 = path[j];
          if (j == path.length - 1) {
            p2 = path[0];
          } else {
            p2 = path[j + 1];
          }
          if (!wordToAdjacents[p1]) {
            wordToAdjacents[p1] = [];
          }
          wordToAdjacents[p1].push(p2);
        }
      }

      $("#numPaths").text(numPaths);

      // add edges
      $.get( '/get/original-edges/' + pos + '/' + size, function( data ) {
        var edges = data.split("\n");
        for (var i = 0; i < edges.length; i++) {
          var edge = edges[i].split("\t")
          var source = JSON.parse(edge[0])[0]
          var targets = JSON.parse(edge[1])

          for (var j = 0; j < targets.length; j++) {
            target = targets[j];



            if (!wordToAdjacents[source] && !wordToAdjacents[target]) {
              // console.log(source)
              // if neither source nor target are in cycle, ignore edge
              continue;
            }

            var color = "gray";
            // make color of edge red if it is in a cycle
            if (wordToAdjacents[source]) {
              var adjWords = wordToAdjacents[source]; // adjacent cycle words
              if (arrayContainsFullWord(adjWords, target)) {
                color = "red"
              }
            }

            var temp = {source: source, target: target, type: "suit", color: color}
            original_links.push(temp)
          }
        }

        draw("original");

      });

    });

  })

  
}

function draw(graphType) {
  var nodes = {};
  var links;
  var spaceId;

  if (graphType == "original") {
    links = original_links;
    spaceId = "#originalSpace";
  }
  else if (graphType == "collapsed") { 
    links = collapsed_links;
    spaceId = "#collapsedSpace";
  }

  // Compute the distinct nodes from the links.
  links.forEach(function(link) {
    var sColor = "gray";
    var tColor = "gray";
    if (graphType == "original") {
      if (wordToAdjacents[link.source]) {
        sColor = "red";
      }
      if (wordToAdjacents[link.target]) {
        tColor = "red";
      }
    } else if (graphType == "collapsed") {
      if (arrayContainsFullWord(link.source, cycle_word)) {
        sColor = "red";
      }
      else if (arrayContainsFullWord(link.target, cycle_word)) {
        tColor = "red";
      }
    }

    link.source = nodes[link.source] || (nodes[link.source] = {name: link.source, color: sColor});
    link.target = nodes[link.target] || (nodes[link.target] = {name: link.target, color: tColor});
  });

  margin = {top: -5, right: -5, bottom: -5, left: -5};
  width = $(".graphSpace").width() - margin.left - margin.right;
  height = $(".graphSpace").height()- margin.top - margin.bottom;
  console.log(height)

  var force = d3.layout.force()
      .charge(-800)
      .linkDistance(140)
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
      .attr("id", function(d) { return graphType + "" + d; })
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
      .attr("marker-end", function(d) { return "url(#" + graphType + "" + d.type + ")"; })
      .style("stroke", function(d) { return d.color; })


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
        if (wordToAdjacents[data.name] && graphType == "original")  {
          console.log(data.name);
          cycle_word = data.name;
          render_collapsed()
        }
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
      .text(function(d) { return d.name; });


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




function render_collapsed() {
  $("#originalSpace").hide();
  $("#originalButton").show();
  $("#collapsedSpace").show();
  $("#collapsedSpace").html("");

  collapsed_links = [];
  // dictionary of words to the words that they touch in a cycle with a
  // forward directed edge
  // e.g {"transformations": ["reforms"]}



  // add edges
  $.get( '/get/collapsed-edges/' + pos + '/' + size, function( data ) {
    var edges = data.split("\n");
    for (var i = 0; i < edges.length; i++) {
      var edge = edges[i].split("\t")
      var source = JSON.parse(edge[0])
      var targets = JSON.parse(edge[1])

      for (var j = 0; j < targets.length; j++) {
        target = targets[j];

        if (!arrayContainsFullWord(source, cycle_word) && !arrayContainsFullWord(target, cycle_word)) {
          // console.log(source)
          // if the cycle word isn't in the source nor target, ignore the edge
          continue;
        } else {
          console.log(source);
          console.log(target)
        }

        var color = "gray";

        var temp = {source: source, target: target, type: "suit", color: color}
        collapsed_links.push(temp)
      }
    }

    draw("collapsed");

  });



}