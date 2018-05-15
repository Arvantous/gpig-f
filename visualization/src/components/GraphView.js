import React from 'react'
//import Graph from "react-graph-vis";
import './GraphView.scss'
import Container from './visual/Container'
import vis from "vis"
import _ from "lodash"
/**
 * The part of the app that holds the tree visualization.
 */

var graph = {
  nodes: [
      {id: 1, label: 'Node 1'},
      {id: 2, label: 'Node 2'},
      {id: 3, label: 'Node 3'},
      {id: 4, label: 'Node 4'},
      {id: 5, label: 'Node 5'}
    ],
  edges: [
      {from: 1, to: 2},
      {from: 1, to: 3},
      {from: 2, to: 4},
      {from: 2, to: 5}
    ]
};


var events = {
    select: function(event) {
        var { nodes, edges } = event;
        //onSelectedAgent(nodes);
    }
}

var options = {
    layout: {
        hierarchical: false
    },
    edges: {
        color: "#000000"
    }
};

function generateGraph(currEdges, currNodes, world){
  var nodes = [];
  var edges = [];
  for(var agent of world.agents){
    nodes.push({id: agent.node_id, label: agent.node_id});
    if (agent.parent_node !== null){
      edges.push({from: agent.node_id, to:agent.parent_node});
    }
  }
  //dynamicly add and removes edges/ nodes
  currNodes.remove(_.differenceBy(currNodes.get(), nodes, 'id'));
  currNodes.add(_.differenceBy(nodes, currNodes.get(), 'id'));
  currEdges.remove(_.differenceWith(currEdges.get(), edges, _.isEqual));
  currEdges.add(_.differenceWith(edges, currEdges.get(), _.isEqual));
}

// const GraphView = ({world, onSelectedAgent }) => (
//   <div className='GraphView'>
//       {/*<input type="button" value="Click Me!" onClick={() => onSelectedAgent('new-agent')}*/}
//       <Graph graph={generateGraph(world)} options={options} events={events} />
//   </div>
// )
class GraphView extends React.Component{
  constructor (props) {
    super(props)
    this.edges = new vis.DataSet([])
    this.nodes = new vis.DataSet([])
  }

  componentDidMount() {
    this.network = new vis.Network(this.el, {}, options);
    this.network.on('select', (event) => {
      var { nodes } = event;
      this.props.onSelectedAgent(nodes[0]);
    })
    this.network.setData({edges: this.edges, nodes: this.nodes});
    generateGraph(this.edges, this.nodes, this.state.world);
  }

  componentWillUnmount() {
    this.network.destroy()
  }

  componentDidUpdate (prevProps, prevState) {
    generateGraph(this.edges, this.nodes, this.state.world)
  }

  render() {
    return <div style={{height:"100%"}} ref={el => this.el = el} />;
  }
}

GraphView.getDerivedStateFromProps = nextProps => nextProps

export default GraphView
