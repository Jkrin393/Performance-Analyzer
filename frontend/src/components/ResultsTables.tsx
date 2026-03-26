//import type { JSX } from 'react'
import type { AnalysisResponse, SecurityMetrics, BestMetrics } from '../types'
import { useState } from 'react'

interface TableProperties {
  results: AnalysisResponse
}

export default function ResultsTables({ results }: TableProperties) {
    const comparison = results.comparisonTable
    const tickerNames = Object.keys(comparison)
    const [showAllRequestedTickers, setShowAllRequestedTickers] = useState(false)

    const metricNames: Array<keyof SecurityMetrics> = [
        'Start Price',
        'End Price',
        'Total Return($)',
        'Total Return(%)',
        'Average Daily Change(%)',
        'Volatility(std dev)',
        'Sharpe Ratio'
    ]
    const bestMetricNames: Array<keyof BestMetrics> = [
        'Start Price',
        'End Price',
        'Total Return(%)',
        'Sharpe Ratio',
    ]
    
    return (
     <div className="results">
        <h3>Best Security: {results.bestSecurity}</h3>
        <table>
        <tbody>
            {bestMetricNames.map((metric) => (
            <tr key={metric}>
              <td>{metric}</td>
              <td>{results.bestMetrics[metric].toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/*button to show/hide all requested tickers*/}
      <button onClick={()=> setShowAllRequestedTickers(!showAllRequestedTickers)}  style={{ display: "block", marginTop: "12px" }}> 
        {showAllRequestedTickers?"▼Hide all requested tickers":"▶Show all requested tickers" }
      </button>
      
      {showAllRequestedTickers && (
      <>
      <h3>All requested tickers:</h3>
      <table>
        <thead>
          <tr>
            <th></th>
            {tickerNames.map((ticker) => (
              <th key={ticker}>{ticker}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {metricNames.map((metric) => (
            <tr key={metric}>
              <td>{metric}</td>
              {tickerNames.map((ticker) => {
                const value = comparison[ticker][metric];
                return(
                  <td key={ticker}>{typeof value==="number"?value.toFixed(2) : value}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      </>
      )}
     </div>
    )

}