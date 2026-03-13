//https://recharts.github.io/

//chart definition
import { LineChart, Line, XAxis, YAxis, CartesianGrid,Tooltip,Legend, } from "recharts"
import type { HistoricalDataMetrics, PriceData } from '../types'

type ChartRow = {
  date: string
} & Record<string, number | string>

interface PriceChartProperties {
  historicalData: HistoricalDataMetrics
}

export default function PriceChart({ historicalData }:PriceChartProperties) {
 

    const symbols=Object.keys(historicalData).slice(0,5)
    if(symbols.length===0) {
        return null
    }
    const dates:string[]=[]
    const firstSymbol=symbols[0]
        
    var i,j
    for (i=0;i<historicalData[firstSymbol].length;++i){
        const price:PriceData=historicalData[firstSymbol][i]
        dates.push(price.Date)
    }

    const chartData: ChartRow[]=[]

    for(i=0;i<dates.length;++i){
        const row:ChartRow={date:dates[i]}

        for(j=0;j<symbols.length;++j){
            const symbol=symbols[j]
            row[symbol]=historicalData[symbol][i]["4. close"]
        }
        chartData.push(row)
    }

    const colors=['#535bf2', '#82ca9d', '#ffc658', '#ff7300', '#a4de6c']

    return (
        <LineChart width={700} height={400} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            {symbols.map((symbol, index) => (
            <Line key={symbol} dataKey={symbol} stroke={colors[index % colors.length]} strokeWidth={2} dot={false}/>
            ))}
        </LineChart>

    )


}