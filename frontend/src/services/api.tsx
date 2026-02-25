import type { AnalysisResponse,SecurityMetrics,BestMetrics } from '../types'

//analyze securities
export async function analyzeSecurities(symbols: string[], days: number, useFakeData: boolean)
{
    const endpoint=useFakeData ? '/api/fakeanalyze':'/api/analyze'
    const apiRequestOptions=
    {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({symbols, days})
    }

    const backendResponse=await fetch(endpoint, apiRequestOptions)

    if(!backendResponse.ok)
    {
        throw new Error("could now analyze securities")
    }
    
    const returnData: AnalysisResponse=await backendResponse.json()
    return returnData

}


//return all tickers
export const loadAllTickers = async (limit: number) => {
  const response = await fetch(`/admin/tickers?limit=${limit}`)
  
  if (!response.ok) {
    throw new Error('Failed to load tickers')
  }
  
  const data = await response.json()
  return data.tickers
}