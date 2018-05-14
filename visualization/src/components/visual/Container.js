import React from 'react'

/**
 * Wraps the included children with a padding space.
 * @param {*} padding the padding around the container elements
 */
const Container = ({ children, padding = '5px' }) => (
  <div style={{ padding }}>{children}</div>
)

export default Container
