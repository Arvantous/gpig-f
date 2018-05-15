import React from 'react'

import './Stepper.scss'

const Stepper = ({ isPlaying, onStep, onPlay, onPause }) => (
  <div className='Stepper'>
    <input type='button' value='Step' disabled={isPlaying} onClick={onStep} />
    <input type='button' value='Play' disabled={isPlaying} onClick={onPlay} />
    <input type='button' value='Pause' disabled={!isPlaying} onClick={onPause} />
  </div>
)

export default Stepper
