# Performance-Analyzer
Compare performance of portfolio investments over time

to run,
set up a virtual environment and run the installs inside the virtual environment

Install backend dependencies: pip install -r requirements.txt  

Install frontend dependencies: npm install

register for a free API key from  https://www.alphavantage.co/support/#

add a 'config.py' file to the base directory and save your API key with variable name 'API_KEY=<your_api_key>  

to run from CLI, run "python cli_main.py <security1> <security2> ...<security5>" seperating the tickers with a space

to run from browser you will need two virtual environments, one for frontend and the other for backend

for backend, "fastapi run app.py"
for frontend, "npm run dev"

then in your browser go to localhost:5173 or 127.0.0.1:5173



