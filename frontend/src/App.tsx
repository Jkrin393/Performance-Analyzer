import { useState } from 'react'
import './App.css'
import type { AnalysisResponse } from './types'

function App(){
  const [symbols, setSymbols]=useState('')
  const [days, setDays]=useState(7)
  const [results, setResults]=useState<AnalysisResponse| null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')


  const handleSubmit=async(event:React.SyntheticEvent<HTMLFormElement>)=>
  {
    event.preventDefault()//preventDefault to prevent app reloading/interupting async call
    setLoading(true)
    setError('')
    
    const symbolArray=symbols.toUpperCase().split(/[\s,]+/)
    
    const payload={
      symbols:symbolArray,
      daysRequested:days,
    }
    const apiRequestOptions={
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload)
    }

    try{
      const backendResponse=await fetch('/api/analyze',apiRequestOptions)
      const returnedData:AnalysisResponse=await backendResponse.json()
      setResults(returnedData)
    }
    catch(error){
      setError('Issue with POST request')
    }
    finally{
      setLoading(false)
    }


  }//event handler end

  return(
    <div className='app'>
      <h1>Security Analyzer</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Requested Symbols</label>
            <input
              type="text"
              value={symbols}
              onChange={(event:React.ChangeEvent<HTMLInputElement>) => setSymbols(event.target.value)} //event.value returns htmlInputEvent, .target specifies calling calling element
            />
          </div>

          <div>
            <label>Days: </label>
              <input
              type="number"
              value={days}
              onChange={(event:React.ChangeEvent<HTMLInputElement>) => setDays(Number(event.target.value))} 
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Loading results' : 'Analyze'}
          </button>
        </form>
        {error && <p className='error'>{error}</p>}

        {results && (
          <pre>{JSON.stringify(results, null, 2)}</pre>
        )}
  </div>
    
    
  )


}///App end

export default App
