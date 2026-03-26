//file for contacting 3rd party APIs

import type { AnalysisResponse,} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

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

    const backendResponse=await fetch(`${API_BASE_URL}${endpoint}`, apiRequestOptions)

    if(!backendResponse.ok)
    {
        throw new Error("could not analyze securities")
    }
    
    const returnData: AnalysisResponse=await backendResponse.json()
    return returnData

}


//return all tickers
export const loadAllTickers = async (limit: number) => {
  const response = await fetch(`${API_BASE_URL}/admin/tickers?limit=${limit}`)
  
  if (!response.ok) 
  {
    throw new Error('Failed to load tickers')
  }
  
  const data = await response.json()
  return data.tickers
}


