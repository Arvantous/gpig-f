import React from 'react'
import vis from 'vis'
import _ from 'lodash'
import './GraphView.scss'

const graphOptions = {
  layout: {
    hierarchical: false
  },
  edges: {
    color: {color:'#000000'}
},
  groups: {
            house: {
                shape: 'icon',
                icon: {
                    code: '🏡',
                    size: 50,
                    color: 'orange'
                }
            },
            infrastructure: {
                shape: 'icon',
                icon: {
                    code: '🏢',
                    size: 50,
                    color: 'cyan'
                }
            },
            cluster: {
                shape: 'icon',
                icon:{
                    code:'☁',
                    size: 50,
                    color: 'white',
                }
            },
            business: {
                shape: 'icon',
                icon: {
                    code: '🏪',
                    size: 50,
                    color: 'orange'
                }
            }
        }

}

function generateGraph (currEdges, currNodes, world) {
  var nodes = []
  var edges = []
  for (var agent of world.agents) {
    nodes.push({id: agent.node_id, label: agent.node_id, group: agent.archetype})
    if (agent.parent_node !== null) {
      edges.push({from: agent.node_id, to: agent.parent_node})
    }
    // add transfer edges
    for(var transfer of agent.transfer_queue){
      if(transfer[2] !== 0){
          edges.push({
              from: transfer[0],
              to: transfer[1],
              label: transfer[2].toString(),
              color: {color:'#1F75FE'},
              arrows:'to',
              dashes:true});
      }
    }

  }
  function compEdges(val, oth){
     return (val.to === oth.to && val.from === oth.from && val.label === oth.label)
  }
  // dynamically add and removes edges/nodes
  currNodes.remove(_.differenceBy(currNodes.get(), nodes, 'id'))
  currNodes.add(_.differenceBy(nodes, currNodes.get(), 'id'))
  currEdges.remove(_.differenceWith(currEdges.get(), edges, compEdges))
  currEdges.add(_.differenceWith(edges, currEdges.get(), compEdges))
  //console.log(currEdges);
}

/**
 * The part of the app that holds the tree visualization.
 */
class GraphView extends React.Component {
  constructor (props) {
    super(props)
    this.el = undefined
    this.edges = new vis.DataSet([])
    this.nodes = new vis.DataSet([])
  }

  componentDidMount () {
    this.network = new vis.Network(this.el, {}, graphOptions)
    this.network.on('select', ({ nodes }) => {
      var node = nodes[0];
      this.props.onSelectedAgent(node)
      //Animate selection
      var options = {
        position: {x:300,y:300},
        scale: 1.5,
        offset: {x:0,y:0},
        animation: true // default duration is 1000ms and default easingFunction is easeInOutQuad.
      };
      if(node !== undefined){
          this.network.focus(node,options);
      }
      else{
          this.network.fit(options);
      }
    })
    this.network.setData({edges: this.edges, nodes: this.nodes})

    generateGraph(this.edges, this.nodes, this.state.world)
  }

  componentWillUnmount () {
    this.network.destroy()
  }

  componentDidUpdate (prevProps, prevState) {
    generateGraph(this.edges, this.nodes, this.state.world)
  }

  render () {
    return <div className='GraphView' ref={el => { this.el = el }} />
  }
}

GraphView.getDerivedStateFromProps = ({ world }) => ({ world })

export default GraphView
