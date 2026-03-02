import type { JSX } from 'react'
import type { AnalysisResponse, SecurityMetrics, BestMetrics } from '../types'

interface TableProperties {
  results: AnalysisResponse
}

export default function ResultsTables({ results }: TableProperties) {
    const comparison = results.comparisonTable
    const tickerNames = Object.keys(comparison)

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

      <h3>All Results:</h3>
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
              {tickerNames.map((ticker) => (
                <td key={ticker}>{comparison[ticker][metric]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
     </div>
    )

}