import React, { useState, type JSX } from 'react'
import './App.css'
import type { AnalysisResponse, SecurityMetrics } from './types'

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
      days:days,
    }
    const apiRequestOptions={
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(payload)
    }
    /*
    try{
      const backendResponse=await fetch('/api/analyze',apiRequestOptions)
      const returnedData:AnalysisResponse=await backendResponse.json()
      console.log('Returned data:', returnedData);
      setResults(returnedData)
    }
    catch(error){
      setError('Issue with POST request')
    }
    finally{
      setLoading(false)
    }*/

    //fake backend data to save API calls to Alpha Vantage
    const loadFakeData=async()=>{
      setLoading(true)
      try{
        const fakeBackendResponse=await fetch('/api/fakeanalyze', apiRequestOptions)
        const fakeBackendData: AnalysisResponse=await fakeBackendResponse.json()
        console.log('Fake Data: ', fakeBackendData)
        
        setResults(fakeBackendData)
      }
      catch(error){
        setError("somehow there was an issue loading fake data")
      }
      finally{
        setLoading(false)
      }
    }
  loadFakeData()


  }//event handler end

  const renderComparisonTable=()=>{
    if(!results)
      return null

    const comparison =results.comparisonTable
    const tickerNames=Object.keys(comparison)
    const metricNames: Array<keyof SecurityMetrics> = [
      'Start Price',
      'End Price',
      'Total Return($)',
      'Total Return(%)',
      'Average Daily Change(%)',
      'Volatility(std dev)',
      'Sharpe Ratio'
    ]

    console.log(tickerNames)

    const metricsTableHeaderCells: JSX.Element[] =[]
      for(let i=0;i<tickerNames.length;++i){
        metricsTableHeaderCells.push(<th key={tickerNames[i]}>{tickerNames[i]}</th>)
      }
    const metricsTableRows: JSX.Element[]=[]
    for(let i=0;i<metricNames.length;++i){
      const metric=metricNames[i]
      const cells: JSX.Element[]=[]
    
      cells.push(<td key="metric">{metric}</td>)

      for(let j=0;j<tickerNames.length;++j){
        const symbol=tickerNames[j]
        const value=comparison[symbol][metric]
        cells.push(<td key={symbol}>{value}</td>)
      }
      metricsTableRows.push(<tr key={metric}>{cells}</tr>)
    }//end of table creation loop


    return(
      <table>
        <thead>
        <tr>
          <th>Metric</th>
          {metricsTableHeaderCells}
        </tr>
        </thead>
        <tbody>{metricsTableRows}</tbody>
      </table>
    )

  }//render function

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
        <div className="results">
          <h2>Best Security: {results.bestSecurity}</h2>
          
          <h3>Metrics: </h3>
            <p>Start Price: {results.bestMetrics['Start Price'].toFixed(2)}</p>
            <p>End Price: {results.bestMetrics['End Price'].toFixed(2)}</p>
            <p>Total Return(%): {results.bestMetrics['Total Return(%)'].toFixed(2)}</p>
            <p>Total Return($): {results.bestMetrics['Total Return($)'].toFixed(2)}</p>
            <p>Sharpe Ratio: {results.bestMetrics['Sharpe Ratio'].toFixed(2)}</p>
        
          <h3>All Results: </h3>
          {renderComparisonTable()}
        
        </div> //results div        

          
          
          //<pre>{JSON.stringify(results, null, 2)}</pre>
        )}
  </div>
    
    
  )


}///App end

export default App
