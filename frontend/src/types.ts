export interface AnalysisResponse {
  comparisonTable: ComparisonTable
  bestSecurity: string
  bestMetrics: BestMetrics
  lastRefreshed: Record<string, string>
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
  'Total Return($)': number
  'Total Return(%)': number
  'Average Daily Change(%)': number
  'Volatility(std dev)': number
  'Sharpe Ratio': number
}

