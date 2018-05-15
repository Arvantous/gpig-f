import React from 'react'

import './GraphView.scss'
import Container from './visual/Container'

/**
 * The part of the app that holds the tree visualization.
 */
const GraphView = ({ world, onSelectedAgent }) => (
  <div className='GraphView'>
    <Container>
      <input type="button" value="Click Me!" onClick={() => onSelectedAgent('new-agent')} />
    </Container>
  </div>
)

export default GraphView
