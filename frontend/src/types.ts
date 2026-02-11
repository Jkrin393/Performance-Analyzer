export interface AnalysisResponse {
  comparisonTable: ComparisonData
  bestSecurity: string
  bestMetrics: BestMetrics
  lastRefreshed: Record<string, string>
}

export interface ComparisonData {
  'Start Price': Record<string, number>
  'End Price': Record<string, number>
  'Total Return($)': Record<string, number>
  'Total Return(%)': Record<string, number>
  'Average Daily Change(%)': Record<string, number>
  'Volatility(std dev)': Record<string, number>
  'Sharpe Ratio': Record<string, number>
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