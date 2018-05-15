import React from 'react'

import './NodeView.scss'
import Container from './visual/Container'

/**
 * The details panel for a selected node.
 */
const NodeView = ({world, selectedAgentId}) => (
  <div className='NodeView'>
    <Container>
      Currently selected: {selectedAgentId || 'nothing'}
    </Container>
  </div>
)

export default NodeView
