export interface AnalysisResponse {
  comparisonTable: ComparisonTable
  bestSecurity: string
  bestMetrics: BestMetrics
  lastRefreshed: Record<string, string>
  historical_data: HistoricalDataMetrics
}
export interface ComparisonTable {
  [symbol: string]: SecurityMetrics 
}

export interface SecurityMetrics {
  'Start Price': number
  'End Price': number
  'Total Return($)': number
  'Total Return(%)': number
  'Average Daily Change(%)': number
  'Volatility(std dev)': number
  'Sharpe Ratio': number
}

export interface BestMetrics {
  'Start Price': number
  'End Price': number
  'Total Return(%)': number
  'Sharpe Ratio': number
}

//types for graphing stock data
export interface HistoricalDataMetrics{
  [symbol:string]:PriceData[]
}

export interface PriceData {
  Date: string
  '4. close': number
}

