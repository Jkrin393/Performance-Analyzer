import { useState } from 'react'
import { loadAllTickers } from '../services/api'

interface Ticker {
  symbol: string
  name: string
}

interface TickerListProperties
{
  onTickerSelect: (symbol: string) => void
}

export default function TickerList({ onTickerSelect }: TickerListProperties)
{
  const [showAllTickers, setShowAllTickers] = useState(false)
  const [allTickers, setAllTickers] = useState<Ticker[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')  
  
    const handleLoadTickers = async () => 
    {
        setLoading(true)
        setError('')

        try
        {
            const tickers=await loadAllTickers(100)
            setAllTickers(tickers)
            setShowAllTickers(true)
        }
        catch(err)
        {
            setError("couldnt load tickers")
            console.error(err)
        }
        finally{
            setLoading(false)
        }

    }
    
    return
    (
        <div className="ticker-list-container"></div>
    )
}