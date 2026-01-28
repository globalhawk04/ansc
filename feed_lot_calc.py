import webbrowser
import os

def generate_feedlot_tool():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedlot Profitability Slider</title>
    <style>
        :root {
            --primary: #2c3e50;
            --accent: #27ae60;
            --danger: #c0392b;
            --bg: #f4f7f6;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); margin: 0; padding: 20px; color: #333; }
        .container { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1fr 350px; gap: 20px; }
        
        /* Cards */
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
        h2 { margin-top: 0; color: var(--primary); font-size: 1.2rem; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        h1 { text-align: center; color: var(--primary); }

        /* Inputs & Sliders */
        .input-group { margin-bottom: 15px; }
        label { display: block; font-weight: 600; font-size: 0.9rem; margin-bottom: 5px; }
        input[type="number"], select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        
        .slider-container { margin-bottom: 20px; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
        .slider-val { font-weight: bold; color: var(--primary); background: #eef2f5; padding: 2px 8px; border-radius: 4px; }
        input[type="range"] { width: 100%; cursor: pointer; accent-color: var(--primary); }

        /* Results Panel */
        .results-panel { position: sticky; top: 20px; height: fit-content; }
        .metric { margin-bottom: 20px; text-align: center; }
        .metric-label { font-size: 0.85rem; color: #666; text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { font-size: 2rem; font-weight: 800; color: var(--primary); }
        .metric-sub { font-size: 0.9rem; color: #888; }
        
        .profit-box { background: var(--primary); color: white; padding: 20px; border-radius: 8px; text-align: center; transition: background 0.3s; }
        .profit-box.positive { background: var(--accent); }
        .profit-box.negative { background: var(--danger); }
        
        @media (max-width: 800px) { .container { grid-template-columns: 1fr; } }
    </style>
</head>
<body>

    <h1>🐄 Cattle Feedlot Decision Aid</h1>

    <div class="container">
        
        <!-- Left Column: Inputs -->
        <div class="main-inputs">
            
            <!-- Strategy Selector -->
            <div class="card">
                <h2>1. Feeding Strategy</h2>
                <div class="input-group">
                    <label>Select Plan Profile</label>
                    <select id="strategySelect" onchange="applyStrategy()">
                        <option value="custom">Custom (Manual Entry)</option>
                        <option value="high_growth" selected>Aggressive Growth (High Energy)</option>
                        <option value="backgrounding">Backgrounding (Forage Based)</option>
                    </select>
                </div>
            </div>

            <!-- The Sliders (Variables) -->
            <div class="card">
                <h2>2. Market Variables (Slide to adjust)</h2>
                
                <div class="slider-container">
                    <div class="slider-header">
                        <label>Purchase Price ($/cwt)</label>
                        <span class="slider-val" id="val_purchase_price">$240</span>
                    </div>
                    <input type="range" id="purchase_price" min="150" max="350" step="1" value="240">
                </div>

                <div class="slider-container">
                    <div class="slider-header">
                        <label>Feed Price ($/ton as fed)</label>
                        <span class="slider-val" id="val_feed_price">$220</span>
                    </div>
                    <input type="range" id="feed_price" min="100" max="500" step="5" value="220">
                    <small style="color:#666">Avg Ration Cost</small>
                </div>

                <div class="slider-container">
                    <div class="slider-header">
                        <label>Est. Sale Price ($/cwt)</label>
                        <span class="slider-val" id="val_sale_price">$185</span>
                    </div>
                    <input type="range" id="sale_price" min="130" max="250" step="1" value="185">
                </div>

                <div class="slider-container">
                    <div class="slider-header">
                        <label>Average Daily Gain (lbs/day)</label>
                        <span class="slider-val" id="val_adg">3.8</span>
                    </div>
                    <input type="range" id="adg" min="1.5" max="5.0" step="0.1" value="3.8">
                </div>

                <div class="slider-container">
                    <div class="slider-header">
                        <label>Interest Rate (%)</label>
                        <span class="slider-val" id="val_interest">7.5%</span>
                    </div>
                    <input type="range" id="interest" min="0" max="15" step="0.25" value="7.5">
                </div>
            </div>

            <!-- Static Setup -->
            <div class="card">
                <h2>3. Lot Setup (Static Inputs)</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div class="input-group">
                        <label>In Weight (lbs)</label>
                        <input type="number" id="in_weight" value="650">
                    </div>
                    <div class="input-group">
                        <label>Target Out Weight (lbs)</label>
                        <input type="number" id="out_weight" value="1400">
                    </div>
                    <div class="input-group">
                        <label>Feed Conversion (F:G)</label>
                        <input type="number" id="fcr" value="6.5" step="0.1">
                    </div>
                    <div class="input-group">
                        <label>Death Loss (%)</label>
                        <input type="number" id="death_loss" value="1.5" step="0.1">
                    </div>
                    <div class="input-group">
                        <label>Vet/Med ($/head)</label>
                        <input type="number" id="vet_cost" value="25">
                    </div>
                    <div class="input-group">
                        <label>Yardage ($/day)</label>
                        <input type="number" id="yardage" value="0.40" step="0.05">
                    </div>
                </div>
            </div>
        </div>

        <!-- Right Column: Results -->
        <div class="results-panel">
            <div class="card profit-box" id="profitBox">
                <div class="metric-label" style="color: rgba(255,255,255,0.8);">Net Profit Per Head</div>
                <div class="metric-value" id="res_profit">$0.00</div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Breakeven Sale Price</div>
                    <div class="metric-value" id="res_be_sale" style="color:#333;">$0.00</div>
                    <div class="metric-sub">To cover all costs</div>
                </div>
                <hr style="border:0; border-top:1px solid #eee;">
                <div class="metric">
                    <div class="metric-label">Cost of Gain</div>
                    <div class="metric-value" id="res_cog" style="color:#333;">$0.00</div>
                    <div class="metric-sub">Per lb of added weight</div>
                </div>
                <hr style="border:0; border-top:1px solid #eee;">
                <div class="metric">
                    <div class="metric-label">Days on Feed</div>
                    <div class="metric-value" id="res_days" style="color:#333;">0</div>
                </div>
            </div>

            <div class="card">
                <h3 style="margin-top:0; font-size:0.9rem;">Cost Breakdown</h3>
                <ul style="padding-left: 20px; font-size: 0.9rem; color: #555; line-height: 1.6;">
                    <li>Cattle Cost: <b id="cost_cattle">$0</b></li>
                    <li>Feed Cost: <b id="cost_feed">$0</b></li>
                    <li>Yardage/Fixed: <b id="cost_yard">$0</b></li>
                    <li>Interest: <b id="cost_interest">$0</b></li>
                    <li>Vet/Death: <b id="cost_vet">$0</b></li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // Data for presets
        const strategies = {
            'high_growth': { adg: 3.8, fcr: 6.5, feed_price: 220, yardage: 0.40 },
            'backgrounding': { adg: 2.2, fcr: 8.5, feed_price: 160, yardage: 0.30 }
        };

        // Inputs
        const inputs = [
            'purchase_price', 'feed_price', 'sale_price', 'adg', 'interest',
            'in_weight', 'out_weight', 'fcr', 'death_loss', 'vet_cost', 'yardage'
        ];

        // Attach listeners
        inputs.forEach(id => {
            const el = document.getElementById(id);
            el.addEventListener('input', () => {
                if(id === 'purchase_price' || id === 'feed_price' || id === 'sale_price' || id === 'adg' || id === 'interest') {
                    // Update the span label next to slider
                    let suffix = '';
                    let prefix = '';
                    if(id === 'interest') suffix = '%';
                    else if (id !== 'adg') prefix = '$';
                    document.getElementById('val_' + id).textContent = prefix + el.value + suffix;
                }
                // If user manually changes a slider, set strategy to custom
                if (['adg', 'fcr', 'feed_price'].includes(id)) {
                    document.getElementById('strategySelect').value = 'custom';
                }
                calculate();
            });
        });

        function applyStrategy() {
            const strat = document.getElementById('strategySelect').value;
            if(strat === 'custom') return;

            const data = strategies[strat];
            
            // Update inputs
            document.getElementById('adg').value = data.adg;
            document.getElementById('fcr').value = data.fcr;
            document.getElementById('feed_price').value = data.feed_price;
            document.getElementById('yardage').value = data.yardage;

            // Update visual labels for sliders
            document.getElementById('val_adg').textContent = data.adg;
            document.getElementById('val_feed_price').textContent = '$' + data.feed_price;

            calculate();
        }

        function calculate() {
            // 1. Get Values
            const purchase_price_cwt = parseFloat(document.getElementById('purchase_price').value);
            const feed_price_ton = parseFloat(document.getElementById('feed_price').value);
            const sale_price_cwt = parseFloat(document.getElementById('sale_price').value);
            const adg = parseFloat(document.getElementById('adg').value);
            const interest_rate = parseFloat(document.getElementById('interest').value);
            
            const in_weight = parseFloat(document.getElementById('in_weight').value);
            const out_weight = parseFloat(document.getElementById('out_weight').value);
            const fcr = parseFloat(document.getElementById('fcr').value);
            const death_loss_pct = parseFloat(document.getElementById('death_loss').value);
            const vet_cost = parseFloat(document.getElementById('vet_cost').value);
            const yardage_per_day = parseFloat(document.getElementById('yardage').value);

            // 2. Core Calculations
            const total_gain = out_weight - in_weight;
            const days_on_feed = total_gain / adg;
            
            // Costs
            const cattle_cost = (purchase_price_cwt / 100) * in_weight;
            
            // Feed Cost = Gain * FeedConversionRatio * (PricePerTon / 2000)
            const total_feed_cost = total_gain * fcr * (feed_price_ton / 2000);
            
            const total_yardage = days_on_feed * yardage_per_day;
            
            // Interest (Simple Interest on Cattle Cost + 1/2 of operating costs)
            // Simplified: Interest on just the cattle cost for the duration
            const interest_cost = cattle_cost * (interest_rate / 100) * (days_on_feed / 365);

            // Death Loss (Cost of buying the animal + feed invested before death)
            // Simplified: We assume we lose X% of the herd, so we divide total costs by (1 - death_loss) later, 
            // OR we subtract death loss from revenue. Let's subtract from revenue (Head Sold).
            const heads_bought = 1;
            const heads_sold = heads_bought * (1 - (death_loss_pct/100));

            const total_cost_per_head_placed = cattle_cost + total_feed_cost + total_yardage + interest_cost + vet_cost;
            
            // Revenue
            const revenue_per_head_placed = (sale_price_cwt / 100) * out_weight * heads_sold;

            const net_profit = revenue_per_head_placed - total_cost_per_head_placed;

            // Metrics
            const cost_of_gain = (total_feed_cost + total_yardage + vet_cost + interest_cost) / total_gain;
            
            // Breakeven Sale Price (cwt)
            // (Total Cost / Total Sold Weight) * 100
            const total_sold_weight = out_weight * heads_sold;
            const be_sale_price = (total_cost_per_head_placed / total_sold_weight) * 100;

            // 3. Update DOM
            const fmt = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
            
            const profitBox = document.getElementById('profitBox');
            document.getElementById('res_profit').textContent = fmt.format(net_profit);
            
            if(net_profit >= 0) {
                profitBox.className = "card profit-box positive";
            } else {
                profitBox.className = "card profit-box negative";
            }

            document.getElementById('res_be_sale').textContent = fmt.format(be_sale_price);
            document.getElementById('res_cog').textContent = fmt.format(cost_of_gain) + "/lb";
            document.getElementById('res_days').textContent = Math.round(days_on_feed);

            // Breakdown
            document.getElementById('cost_cattle').textContent = fmt.format(cattle_cost);
            document.getElementById('cost_feed').textContent = fmt.format(total_feed_cost);
            document.getElementById('cost_yard').textContent = fmt.format(total_yardage);
            document.getElementById('cost_interest').textContent = fmt.format(interest_cost);
            
            // Calculate implied death cost for breakdown visualization
            const death_cost_implied = (revenue_per_head_placed / heads_sold) - revenue_per_head_placed; // Lost revenue
            document.getElementById('cost_vet').textContent = fmt.format(vet_cost + death_cost_implied) + " (Inc. D.L.)";
        }

        // Init
        calculate();
    </script>
</body>
</html>
    """

    filename = "cattle_feedlot_calculator.html"
    with open(filename, "w") as f:
        f.write(html_content)
    
    print(f"Success! File created: {filename}")
    print("Opening in browser...")
    
    # Try to open automatically
    try:
        webbrowser.open('file://' + os.path.realpath(filename))
    except:
        print("Could not open browser automatically. Please find the file and double-click it.")

if __name__ == "__main__":
    generate_feedlot_tool()
