//file for contacting 3rd party APIs

import type { AnalysisResponse,} from '../types'

const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL //||(import.meta.env.MODE==='development' ? 'http://localhost:8000':'')

if(!BACKEND_BASE_URL && import.meta.env.VITE_BACKEND_BASE_URL !=='development'){
  throw new Error(
    'VITE_API_URL is not set. Login to Vercel options to specify the path'
  );
}

//analyze securities
export async function analyzeSecurities(symbols: string[], days: number, useFakeData: boolean): Promise<AnalysisResponse>
{
    
    const endpoint=useFakeData ? '/api/fakeanalyze':'/api/analyze'
    const apiRequestOptions=
    {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({symbols, days})
    }

    try{
      const backendResponse=await fetch(`${BACKEND_BASE_URL}${endpoint}`, apiRequestOptions)
      const responseData = await backendResponse.json().catch(()=>null);//catch lambda changes failed json parse to null object

      //pass errors originating in the backend (200 errors where a response was received but the response itself is an error)
      if(!backendResponse.ok)
      {
        if(responseData && responseData.error)
          {
            throw new Error(responseData.error.toString().trim());
          } 
          else
          {
            throw new Error("backend returned an unknown error");
          }
      }

      //const returnData: AnalysisResponse=await backendResponse.json()
      const returnData: AnalysisResponse = responseData as AnalysisResponse;
      return returnData;

    }catch (error: unknown)
    {
      if (error instanceof Error)
      {
        const networkErrorMessages = ['Failed to fetch', 'NetworkError'];//most common network error text
        let isNetworkError=false;
        for(const msg of networkErrorMessages)
        {
          if(error.message.includes(msg))
          {
            isNetworkError=true;
            break;
          }
        }
        if(isNetworkError)
          throw new Error('Could not communicate with backend. Check it is running and reachable(dont forget CORS issues)');
        else
          throw error
      }
    throw new Error('Unexpected error occurred while communicating with backend');

    }

}


//return all tickers
export const loadAllTickers = async (limit: number) => {
  const response = await fetch(`${BACKEND_BASE_URL}/admin/tickers?limit=${limit}`)
  
  if (!response.ok) 
  {
    throw new Error('Failed to load tickers')
  }
  
  const data = await response.json()
  return data.tickers
}


