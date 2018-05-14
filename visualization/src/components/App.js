import React from 'react'

import './App.scss'
import GraphView from './GraphView'
import NodeView from './NodeView'

/**
 * Basically the entry-point for the app.
 */
class App extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      world: undefined
    }
  }

  componentDidMount () {
    this.timerID = setInterval(() => this.tick(), 1000)
  }

  componentWillUnmount () {
    clearInterval(this.timerID)
  }

  tick () {
    console.log('tick')
  }

  render () {
    return (
      <div className='App'>
        <div className='App__GraphView'><GraphView /></div>
        <div className='App__NodeView'><NodeView /></div>
      </div>
    )
  }
}

export default App
