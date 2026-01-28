import webbrowser
import os

def generate_tamu_feedlot_optimizer():
    """
    Generates the Texas A&M branded Feedlot Optimizer HTML file
    and opens it in the default web browser.
    """
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Texas A&M Feedlot Optimizer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Bree+Serif:wght@400&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        /* Texas A&M Brand Colors */
        :root {
            --tamu-maroon: #500000;
            --tamu-white: #FFFFFF;
            --tamu-gray: #3C3C3C;
            --tamu-light-gray: #D3D3D3;
            --tamu-accent: #FFCC00; /* Aggie Gold for accents */
            --tamu-bg: #F5F5F5;
            --cattle-orange: #500000; /* For cattle-specific inputs */
            --success: #4A7729;
            --warning: #C65D00;
            --danger: #9D2235;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body { 
            font-family: 'Open Sans', sans-serif;
            background: var(--tamu-bg);
            color: var(--tamu-gray);
            padding: 20px;
            line-height: 1.6;
        }

        /* Typography - Texas A&M uses Bree Serif for headers */
        h1, h2, h3, h4 {
            font-family: 'Bree Serif', serif;
            color: var(--tamu-maroon);
            font-weight: 400;
        }

        h1 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }

        .brand-tagline {
            text-align: center;
            color: var(--tamu-gray);
            font-size: 0.9rem;
            margin-bottom: 30px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            display: grid; 
            grid-template-columns: 1fr 1fr 350px; 
            gap: 20px;
        }
        
        h2 { 
            margin: 0 0 20px 0;
            font-size: 1.5rem;
            padding-bottom: 12px;
            border-bottom: 3px solid var(--tamu-maroon);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .sub-header { 
            font-family: 'Open Sans', sans-serif;
            font-size: 0.75rem;
            color: var(--tamu-gray);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Cards */
        .card { 
            background: var(--tamu-white);
            padding: 25px;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(80, 0, 0, 0.08);
            height: fit-content;
            border-top: 4px solid var(--tamu-maroon);
        }
        
        /* Ingredient Rows */
        .ingredient-row { 
            display: grid;
            grid-template-columns: 1.5fr 1.5fr 1fr;
            gap: 15px;
            align-items: start;
            margin-bottom: 18px;
            padding-bottom: 18px;
            border-bottom: 1px solid var(--tamu-light-gray);
        }

        .ingredient-row:last-child { 
            border-bottom: none;
        }

        .ingredient-col label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--tamu-maroon);
            font-size: 0.9rem;
        }

        .ingredient-col small {
            display: block;
            font-size: 0.75rem;
            color: var(--tamu-gray);
            margin-top: 4px;
        }
        
        /* Slider Styling */
        .slider-wrapper { 
            margin-bottom: 20px;
        }

        .slider-header { 
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--tamu-maroon);
        }

        .slider-val { 
            color: var(--tamu-maroon);
            font-weight: 700;
            background: #FFF5E6;
            padding: 3px 10px;
            border-radius: 3px;
            border: 1px solid var(--tamu-accent);
            font-size: 0.95rem;
        }

        .cattle-val { 
            color: var(--tamu-white);
            background: var(--cattle-orange);
            border: 1px solid var(--cattle-orange);
        }
        
        input[type="range"] { 
            width: 100%;
            height: 8px;
            cursor: pointer;
            -webkit-appearance: none;
            appearance: none;
            background: var(--tamu-light-gray);
            border-radius: 4px;
            outline: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            background: var(--tamu-maroon);
            cursor: pointer;
            border-radius: 50%;
            border: 2px solid var(--tamu-white);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            background: var(--tamu-maroon);
            cursor: pointer;
            border-radius: 50%;
            border: 2px solid var(--tamu-white);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        input[type="range"].cattle-slider::-webkit-slider-thumb {
            background: var(--cattle-orange);
        }

        input[type="range"].cattle-slider::-moz-range-thumb {
            background: var(--cattle-orange);
        }

        /* Ration Summary */
        .ration-summary { 
            background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E6 100%);
            padding: 18px;
            border-radius: 4px;
            margin-top: 15px;
            border: 2px solid var(--tamu-accent);
        }

        .ration-metric { 
            display: flex;
            justify-content: space-between;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--tamu-gray);
        }

        .ration-metric span:last-child {
            color: var(--tamu-maroon);
            font-size: 1.1rem;
        }

        .warn-text { 
            color: var(--danger);
            font-size: 0.8rem;
            display: none;
            margin-top: 8px;
            font-weight: 600;
        }

        /* Results Panel */
        .results-col { 
            display: flex;
            flex-direction: column;
            gap: 15px;
            position: sticky;
            top: 20px;
        }

        .profit-card { 
            background: var(--tamu-maroon);
            color: var(--tamu-white);
            padding: 30px 25px;
            border-radius: 4px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(80, 0, 0, 0.2);
        }

        .profit-card.positive { 
            background: var(--success);
        }

        .profit-card.negative { 
            background: var(--danger);
        }
        
        .big-number { 
            font-family: 'Bree Serif', serif;
            font-size: 2.8rem;
            font-weight: 400;
            margin: 15px 0;
            letter-spacing: -1px;
        }

        .lbl { 
            font-size: 0.85rem;
            text-transform: uppercase;
            opacity: 0.95;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .analysis-row { 
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid var(--tamu-light-gray);
            font-size: 0.9rem;
        }

        .analysis-row:last-child {
            border-bottom: none;
        }

        .analysis-row span {
            color: var(--tamu-gray);
        }

        .analysis-row strong {
            color: var(--tamu-maroon);
            font-weight: 700;
        }

        .tip-card {
            background: linear-gradient(135deg, #FFF9F0 0%, #FFF5E6 100%);
            padding: 20px;
            border-radius: 4px;
            border-left: 4px solid var(--tamu-accent);
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        .tip-card h4 {
            margin: 0 0 12px 0;
            color: var(--tamu-maroon);
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tip-card p {
            font-size: 0.88rem;
            margin: 0;
            color: var(--tamu-gray);
            line-height: 1.6;
        }

        .tip-card strong {
            color: var(--tamu-maroon);
        }

        hr {
            border: 0;
            border-top: 2px solid var(--tamu-light-gray);
            margin: 20px 0;
        }

        /* Footer */
        .footer {
            grid-column: 1 / -1;
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid var(--tamu-light-gray);
            color: var(--tamu-gray);
            font-size: 0.85rem;
        }

        .footer strong {
            color: var(--tamu-maroon);
        }
        
        @media (max-width: 1100px) { 
            .container { 
                grid-template-columns: 1fr;
            }
            
            .results-col {
                position: relative;
                top: 0;
            }

            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>

    <h1>🐂 Texas A&M Feedlot Optimizer</h1>
    <div class="brand-tagline">Department of Animal Science | AgriLife Extension</div>

    <div class="container">

        <!-- COLUMN 1: RATION BUILDER -->
        <div class="card">
            <h2>
                Feed Ration Builder
                <span class="sub-header">Formulate Your Diet</span>
            </h2>

            <!-- Corn -->
            <div class="ingredient-row">
                <div class="ingredient-col">
                    <label>Corn Price</label>
                    <input type="range" id="price_corn_bu" min="3.00" max="9.00" step="0.10" value="5.50" oninput="updateFeed()">
                    <small>$<span id="lbl_corn_bu">5.50</span> per bushel</small>
                </div>
                <div class="ingredient-col">
                    <label>Inclusion Rate</label>
                    <input type="range" id="pct_corn" min="0" max="100" step="5" value="60" oninput="updateFeed()">
                    <small><span id="lbl_pct_corn">60</span>% of ration</small>
                </div>
                <div class="ingredient-col">
                    <label>Cost/Ton</label>
                    <div id="cost_corn_ton" style="font-size:1.1rem; color: var(--tamu-maroon); font-weight: 700; margin-top: 8px;">$196</div>
                </div>
            </div>

            <!-- DDGS -->
            <div class="ingredient-row">
                <div class="ingredient-col">
                    <label>DDGS Price</label>
                    <input type="range" id="price_ddgs" min="100" max="400" step="5" value="220" oninput="updateFeed()">
                    <small>$<span id="lbl_ddgs">220</span> per ton</small>
                </div>
                <div class="ingredient-col">
                    <label>Inclusion Rate</label>
                    <input type="range" id="pct_ddgs" min="0" max="100" step="5" value="20" oninput="updateFeed()">
                    <small><span id="lbl_pct_ddgs">20</span>% of ration</small>
                </div>
                <div class="ingredient-col">
                    <label>Cost/Ton</label>
                    <div id="cost_ddgs_ton" style="font-size:1.1rem; color: var(--tamu-maroon); font-weight: 700; margin-top: 8px;">$220</div>
                </div>
            </div>

            <!-- Silage/Roughage -->
            <div class="ingredient-row">
                <div class="ingredient-col">
                    <label>Silage/Hay Price</label>
                    <input type="range" id="price_silage" min="30" max="250" step="5" value="55" oninput="updateFeed()">
                    <small>$<span id="lbl_silage">55</span> per ton</small>
                </div>
                <div class="ingredient-col">
                    <label>Inclusion Rate</label>
                    <input type="range" id="pct_silage" min="0" max="100" step="5" value="15" oninput="updateFeed()">
                    <small><span id="lbl_pct_silage">15</span>% of ration</small>
                </div>
                <div class="ingredient-col">
                    <label>Cost/Ton</label>
                    <div id="cost_silage_ton" style="font-size:1.1rem; color: var(--tamu-maroon); font-weight: 700; margin-top: 8px;">$55</div>
                </div>
            </div>

            <!-- Supplement -->
            <div class="ingredient-row">
                <div class="ingredient-col">
                    <label>Supplement Price</label>
                    <input type="range" id="price_supp" min="200" max="800" step="10" value="450" oninput="updateFeed()">
                    <small>$<span id="lbl_supp">450</span> per ton</small>
                </div>
                <div class="ingredient-col">
                    <label>Inclusion Rate</label>
                    <input type="range" id="pct_supp" min="0" max="100" step="1" value="5" oninput="updateFeed()">
                    <small><span id="lbl_pct_supp">5</span>% of ration</small>
                </div>
                <div class="ingredient-col">
                    <label>Cost/Ton</label>
                    <div id="cost_supp_ton" style="font-size:1.1rem; color: var(--tamu-maroon); font-weight: 700; margin-top: 8px;">$450</div>
                </div>
            </div>

            <div class="ration-summary">
                <div class="ration-metric">
                    <span>Blended Ration Cost:</span>
                    <span id="final_ration_cost">$0.00 / ton</span>
                </div>
                <div class="ration-metric" style="font-weight:normal; font-size:0.9rem;">
                    <span>Total Inclusion:</span>
                    <span id="total_pct_display">100%</span>
                </div>
                <div id="pct_warning" class="warn-text">⚠️ Warning: Ingredients must sum to 100%</div>
            </div>
        </div>

        <!-- COLUMN 2: CATTLE PARAMETERS -->
        <div class="card">
            <h2>
                Cattle Performance
                <span class="sub-header">Adjust Parameters</span>
            </h2>
            
            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Purchase Price</label>
                    <span class="slider-val cattle-val" id="lbl_cattle_price">$240/cwt</span>
                </div>
                <input type="range" id="cattle_price" class="cattle-slider" min="150" max="350" step="1" value="240" oninput="calculate()">
            </div>

            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Sale Price</label>
                    <span class="slider-val cattle-val" id="lbl_sale_price">$185/cwt</span>
                </div>
                <input type="range" id="sale_price" class="cattle-slider" min="140" max="260" step="1" value="185" oninput="calculate()">
            </div>

            <hr>

            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Average Daily Gain (ADG)</label>
                    <span class="slider-val cattle-val" id="lbl_adg">3.8 lbs</span>
                </div>
                <input type="range" id="adg" class="cattle-slider" min="1.5" max="5.5" step="0.1" value="3.8" oninput="calculate()">
            </div>

            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Feed Conversion Ratio (F:G)</label>
                    <span class="slider-val cattle-val" id="lbl_fcr">6.5:1</span>
                </div>
                <input type="range" id="fcr" class="cattle-slider" min="4.0" max="12.0" step="0.1" value="6.5" oninput="calculate()">
                <small style="color: var(--tamu-gray); font-size:0.75rem; display: block; margin-top: 4px;">Pounds of feed per pound of gain</small>
            </div>

            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Initial Weight</label>
                    <span class="slider-val cattle-val" id="lbl_in_weight">650 lbs</span>
                </div>
                <input type="range" id="in_weight" class="cattle-slider" min="300" max="1000" step="10" value="650" oninput="calculate()">
            </div>

            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Target Finish Weight</label>
                    <span class="slider-val cattle-val" id="lbl_out_weight">1400 lbs</span>
                </div>
                <input type="range" id="out_weight" class="cattle-slider" min="1000" max="1800" step="10" value="1400" oninput="calculate()">
            </div>

            <hr>

            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Daily Yardage Cost</label>
                    <span class="slider-val cattle-val" id="lbl_yardage">$0.40/day</span>
                </div>
                <input type="range" id="yardage" class="cattle-slider" min="0.10" max="1.00" step="0.05" value="0.40" oninput="calculate()">
            </div>

            <div class="slider-wrapper">
                <div class="slider-header">
                    <label>Interest Rate (Annual)</label>
                    <span class="slider-val cattle-val" id="lbl_interest">8.0%</span>
                </div>
                <input type="range" id="interest" class="cattle-slider" min="0" max="15" step="0.25" value="8.0" oninput="calculate()">
            </div>

        </div>

        <!-- COLUMN 3: RESULTS -->
        <div class="results-col">
            
            <div class="profit-card" id="main_card">
                <div class="lbl">Net Profit Per Head</div>
                <div class="big-number" id="res_profit">$0.00</div>
                <div class="lbl" id="res_roi">ROI: 0.0%</div>
            </div>

            <div class="card">
                <h2 style="font-size: 1.2rem; margin-bottom: 15px;">Performance Metrics</h2>
                
                <div class="analysis-row">
                    <span>Days on Feed</span>
                    <strong id="res_days">0 days</strong>
                </div>
                <div class="analysis-row">
                    <span>Total Cost of Gain</span>
                    <strong id="res_cog">$0.00/lb</strong>
                </div>
                <div class="analysis-row">
                    <span>Feed Cost Only</span>
                    <strong id="res_cog_feed">$0.00/lb</strong>
                </div>
                <div class="analysis-row">
                    <span>Breakeven Sale Price</span>
                    <strong id="res_be_sale">$0.00/cwt</strong>
                </div>
                <div class="analysis-row">
                    <span>Breakeven Purchase</span>
                    <strong id="res_be_buy">$0.00/cwt</strong>
                </div>
            </div>

            <div class="tip-card">
                <h4>💡 Optimization Insight</h4>
                <p>
                    <strong>Lower feed costs don't guarantee higher profits.</strong> 
                    Adjust ration costs in Column 1, then observe how changes to ADG and F:G 
                    in Column 2 impact overall profitability. Performance matters more than price alone.
                </p>
            </div>
        </div>
    </div>

    <div class="footer">
        <strong>Texas A&M AgriLife Extension Service</strong><br>
        Educational tool for feedlot economics analysis | For demonstration purposes
    </div>

    <script>
        // Feed Ration Logic
        let currentRationCostPerTon = 0;

        function updateFeed() {
            // Get prices
            const price_corn_bu = parseFloat(document.getElementById('price_corn_bu').value);
            const price_ddgs = parseFloat(document.getElementById('price_ddgs').value);
            const price_silage = parseFloat(document.getElementById('price_silage').value);
            const price_supp = parseFloat(document.getElementById('price_supp').value);

            // Get inclusion percentages
            const pct_corn = parseFloat(document.getElementById('pct_corn').value);
            const pct_ddgs = parseFloat(document.getElementById('pct_ddgs').value);
            const pct_silage = parseFloat(document.getElementById('pct_silage').value);
            const pct_supp = parseFloat(document.getElementById('pct_supp').value);

            // Update price labels
            document.getElementById('lbl_corn_bu').innerText = price_corn_bu.toFixed(2);
            document.getElementById('lbl_ddgs').innerText = price_ddgs;
            document.getElementById('lbl_silage').innerText = price_silage;
            document.getElementById('lbl_supp').innerText = price_supp;

            // Update percentage labels
            document.getElementById('lbl_pct_corn').innerText = pct_corn;
            document.getElementById('lbl_pct_ddgs').innerText = pct_ddgs;
            document.getElementById('lbl_pct_silage').innerText = pct_silage;
            document.getElementById('lbl_pct_supp').innerText = pct_supp;

            // Convert corn from bushels to tons (56 lbs/bu = 35.71 bu/ton)
            const CORN_BU_PER_TON = 35.71;
            const price_corn_ton = price_corn_bu * CORN_BU_PER_TON;
            document.getElementById('cost_corn_ton').innerText = "$" + Math.round(price_corn_ton);
            document.getElementById('cost_ddgs_ton').innerText = "$" + price_ddgs;
            document.getElementById('cost_silage_ton').innerText = "$" + price_silage;
            document.getElementById('cost_supp_ton').innerText = "$" + price_supp;

            // Validate total percentage
            const total_pct = pct_corn + pct_ddgs + pct_silage + pct_supp;
            const pct_display = document.getElementById('total_pct_display');
            const warn = document.getElementById('pct_warning');
            
            pct_display.innerText = total_pct + "%";
            
            if (total_pct !== 100) {
                pct_display.style.color = "var(--danger)";
                warn.style.display = "block";
            } else {
                pct_display.style.color = "var(--success)";
                warn.style.display = "none";
            }

            // Calculate weighted average ration cost
            const cost_corn = price_corn_ton * (pct_corn / 100);
            const cost_ddgs = price_ddgs * (pct_ddgs / 100);
            const cost_silage = price_silage * (pct_silage / 100);
            const cost_supp = price_supp * (pct_supp / 100);

            currentRationCostPerTon = cost_corn + cost_ddgs + cost_silage + cost_supp;

            document.getElementById('final_ration_cost').innerText = "$" + currentRationCostPerTon.toFixed(2) + " / ton";

            calculate();
        }

        // Profit Calculation Logic
        function calculate() {
            // Get all inputs
            const cattle_price_cwt = parseFloat(document.getElementById('cattle_price').value);
            const sale_price_cwt = parseFloat(document.getElementById('sale_price').value);
            const adg = parseFloat(document.getElementById('adg').value);
            const fcr = parseFloat(document.getElementById('fcr').value);
            const in_weight = parseFloat(document.getElementById('in_weight').value);
            const out_weight = parseFloat(document.getElementById('out_weight').value);
            const yardage = parseFloat(document.getElementById('yardage').value);
            const interest_rate = parseFloat(document.getElementById('interest').value);

            // Update all cattle parameter labels
            document.getElementById('lbl_cattle_price').innerText = "$" + cattle_price_cwt + "/cwt";
            document.getElementById('lbl_sale_price').innerText = "$" + sale_price_cwt + "/cwt";
            document.getElementById('lbl_adg').innerText = adg.toFixed(1) + " lbs";
            document.getElementById('lbl_fcr').innerText = fcr.toFixed(1) + ":1";
            document.getElementById('lbl_in_weight').innerText = in_weight + " lbs";
            document.getElementById('lbl_out_weight').innerText = out_weight + " lbs";
            document.getElementById('lbl_yardage').innerText = "$" + yardage.toFixed(2) + "/day";
            document.getElementById('lbl_interest').innerText = interest_rate.toFixed(2) + "%";

            // Calculate performance metrics
            const total_gain = out_weight - in_weight;
            
            if (total_gain <= 0) {
                document.getElementById('res_profit').innerText = "Invalid Weights";
                return;
            }
            
            const days_on_feed = total_gain / adg;

            // Calculate feed costs
            const total_feed_lbs = total_gain * fcr;
            const feed_cost_total = total_feed_lbs * (currentRationCostPerTon / 2000);

            // Calculate other costs
            const cattle_cost = (cattle_price_cwt / 100) * in_weight;
            const yardage_cost = days_on_feed * yardage;
            const vet_cost = 25; // Fixed veterinary cost
            const interest_cost = (cattle_cost + (feed_cost_total / 2)) * (interest_rate / 100) * (days_on_feed / 365);

            // Total costs and revenue
            const total_cost = cattle_cost + feed_cost_total + yardage_cost + vet_cost + interest_cost;
            const revenue = (sale_price_cwt / 100) * out_weight;
            const profit = revenue - total_cost;
            const roi = (profit / total_cost) * 100;

            // Performance metrics
            const cog_total = (total_cost - cattle_cost) / total_gain;
            const cog_feed = feed_cost_total / total_gain;
            const be_sale = (total_cost / out_weight) * 100;
            const be_buy = ((revenue - (total_cost - cattle_cost)) / in_weight) * 100;

            // Update UI
            const fmt = new Intl.NumberFormat('en-US', { 
                style: 'currency', 
                currency: 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });

            const elProfit = document.getElementById('res_profit');
            const elCard = document.getElementById('main_card');
            
            elProfit.innerText = fmt.format(profit);
            document.getElementById('res_roi').innerText = "ROI: " + roi.toFixed(1) + "%";
            document.getElementById('res_days').innerText = Math.round(days_on_feed) + " days";

            // Color-code profit card
            if (profit >= 0) {
                elCard.className = "profit-card positive";
            } else {
                elCard.className = "profit-card negative";
            }

            document.getElementById('res_cog').innerText = fmt.format(cog_total) + "/lb";
            document.getElementById('res_cog_feed').innerText = fmt.format(cog_feed) + "/lb";
            document.getElementById('res_be_sale').innerText = fmt.format(be_sale) + "/cwt";
            document.getElementById('res_be_buy').innerText = fmt.format(be_buy) + "/cwt";
        }

        // Initialize on page load
        updateFeed();
    </script>
</body>
</html>
"""

    # Write the HTML file
    filename = "tamu_feedlot_optimizer.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Success! Created: {filename}")
    print(f"📍 Location: {os.path.abspath(filename)}")
    
    # Open in default web browser
    try:
        filepath = 'file://' + os.path.realpath(filename)
        webbrowser.open(filepath)
        print(f"🌐 Opening in browser: {filepath}")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"💡 Please open the file manually: {filename}")

if __name__ == "__main__":
    generate_tamu_feedlot_optimizer()