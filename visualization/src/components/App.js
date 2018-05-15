import React from 'react'

import './App.scss'
import GraphView from './GraphView'
import NodeView from './NodeView'

const ENGINE_URL = 'http://localhost:5000'

/**
 * Basically the entry-point for the app.
 */
class App extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      world: {agents: []},
      selectedAgentId: undefined
    }
    this.tick();
  }

  componentDidMount () {
    this.timerID = setInterval(() => this.tick(), 1000)
  }

  componentWillUnmount () {
    clearInterval(this.timerID)
  }

  tick () {
    fetch(ENGINE_URL)
      .then(res => res.json())
      .then((world) => {
        this.setState({...this.state, world})
      })
  }

  onSelectedAgent (newAgentId) {
    this.setState({...this.state, selectedAgentId: newAgentId})
  }

  render () {
    return (
      <div className='App'>
        <div className='App__GraphView'>
          <GraphView
            {...this.state}
            onSelectedAgent={newAgent => this.onSelectedAgent(newAgent)}
          />
        </div>
        <div className='App__NodeView'>
          <NodeView {...this.state} />
        </div>
      </div>
    )
  }
}

export default App
