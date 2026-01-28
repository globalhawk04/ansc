import webbrowser
import os

def create_professional_rumen_simulation():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rumen Optimization Platform</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
            color: #1a202c;
            line-height: 1.6;
        }
        
        /* Top Navigation Bar */
        .navbar {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            padding: 0 32px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .navbar-brand {
            font-size: 1.4rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        .navbar-subtitle {
            font-size: 0.85rem;
            opacity: 0.9;
            margin-left: 16px;
            padding-left: 16px;
            border-left: 1px solid rgba(255,255,255,0.3);
        }
        
        .container { 
            max-width: 1800px; 
            margin: 0 auto; 
            padding: 24px;
        }
        
        /* Control Panel */
        .control-panel {
            background: white;
            border-radius: 8px;
            padding: 20px 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
        }
        
        .control-header {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #6b7280;
            font-weight: 600;
            margin-bottom: 16px;
        }
        
        .scenario-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }
        
        .scenario-btn {
            padding: 12px 20px;
            border: 2px solid #e5e7eb;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.2s;
            text-align: left;
            color: #374151;
        }
        
        .scenario-btn:hover {
            border-color: #3b82f6;
            background: #eff6ff;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
        }
        
        .scenario-btn:active {
            transform: translateY(0);
        }
        
        .scenario-label {
            display: block;
            font-size: 0.7rem;
            text-transform: uppercase;
            color: #9ca3af;
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }
        
        /* Main Layout */
        .main-grid {
            display: grid;
            grid-template-columns: 420px 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }
        
        /* Feed Configuration Panel */
        .config-panel {
            background: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            height: fit-content;
        }
        
        .panel-header {
            font-size: 1.1rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid #f3f4f6;
        }
        
        .feed-control {
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid #f3f4f6;
        }
        
        .feed-control:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }
        
        .feed-label-row {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 6px;
        }
        
        .feed-name {
            font-weight: 600;
            font-size: 0.95rem;
            color: #111827;
        }
        
        .feed-value {
            font-weight: 700;
            font-size: 0.9rem;
            color: #1e40af;
            font-family: 'Courier New', monospace;
        }
        
        .feed-meta {
            font-size: 0.75rem;
            color: #6b7280;
            margin-bottom: 10px;
            line-height: 1.4;
        }
        
        .feed-meta code {
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.7rem;
        }
        
        input[type=range] {
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #e5e7eb;
            outline: none;
            -webkit-appearance: none;
        }
        
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #1e40af;
            cursor: pointer;
            border: 2px solid white;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
        }
        
        input[type=range]::-moz-range-thumb {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #1e40af;
            cursor: pointer;
            border: 2px solid white;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* Metrics Dashboard */
        .metrics-section {
            display: grid;
            gap: 24px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 16px;
        }
        
        .metric-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        }
        
        .metric-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            color: #6b7280;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #111827;
            font-family: 'Courier New', monospace;
        }
        
        .metric-unit {
            font-size: 0.85rem;
            color: #6b7280;
            margin-left: 4px;
        }
        
        .metric-status {
            font-size: 0.7rem;
            margin-top: 6px;
            padding: 3px 8px;
            border-radius: 4px;
            display: inline-block;
            font-weight: 600;
        }
        
        .status-optimal {
            background: #d1fae5;
            color: #065f46;
        }
        
        .status-warning {
            background: #fef3c7;
            color: #92400e;
        }
        
        .status-critical {
            background: #fee2e2;
            color: #991b1b;
        }
        
        /* Chart Section */
        .chart-section {
            background: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
        }
        
        .chart-header {
            font-size: 1rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 20px;
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            width: 100%;
        }
        
        /* Analysis Report */
        .analysis-section {
            background: white;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
        }
        
        .analysis-header {
            font-size: 1rem;
            font-weight: 700;
            color: #111827;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #f3f4f6;
        }
        
        .summary-panel {
            background: #f8fafc;
            border-left: 4px solid #1e40af;
            padding: 16px;
            margin-bottom: 20px;
            border-radius: 4px;
            font-size: 0.875rem;
        }
        
        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .summary-row:last-child {
            margin-bottom: 0;
            padding-top: 8px;
            border-top: 1px solid #e5e7eb;
            font-weight: 600;
        }
        
        .summary-label {
            color: #6b7280;
        }
        
        .summary-value {
            font-weight: 600;
            color: #111827;
        }
        
        .findings-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .finding {
            padding: 14px 16px;
            border-radius: 6px;
            font-size: 0.875rem;
            line-height: 1.6;
            border-left: 4px solid;
        }
        
        .finding-optimal {
            background: #f0fdf4;
            border-color: #10b981;
            color: #065f46;
        }
        
        .finding-info {
            background: #eff6ff;
            border-color: #3b82f6;
            color: #1e40af;
        }
        
        .finding-warning {
            background: #fffbeb;
            border-color: #f59e0b;
            color: #92400e;
        }
        
        .finding-critical {
            background: #fef2f2;
            border-color: #ef4444;
            color: #991b1b;
        }
        
        .finding-title {
            font-weight: 700;
            margin-bottom: 4px;
            display: block;
        }
        
        /* Footer */
        .reference-section {
            background: white;
            border-radius: 8px;
            padding: 20px 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            margin-top: 24px;
        }
        
        .reference-header {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #6b7280;
            font-weight: 600;
            margin-bottom: 12px;
        }
        
        .reference-content {
            font-size: 0.8rem;
            color: #6b7280;
            line-height: 1.8;
        }
        
        .reference-content strong {
            color: #374151;
            font-weight: 600;
        }
        
        /* Responsive */
        @media (max-width: 1400px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
            
            .metrics-grid {
                grid-template-columns: repeat(3, 1fr);
            }
            
            .scenario-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        @media (max-width: 768px) {
            .metrics-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .scenario-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>

<div class="navbar">
    <div style="display: flex; align-items: center;">
        <div class="navbar-brand">Rumen Optimization Platform</div>
        <div class="navbar-subtitle">Fermentation Kinetics & Associative Effects Analysis</div>
    </div>
</div>

<div class="container">
    
    <!-- Scenario Selector -->
    <div class="control-panel">
        <div class="control-header">Preset Configurations</div>
        <div class="scenario-grid">
            <button class="scenario-btn" onclick="loadScenario('balanced')">
                <span class="scenario-label">Standard</span>
                Balanced Diet
            </button>
            <button class="scenario-btn" onclick="loadScenario('feedlot')">
                <span class="scenario-label">High Energy</span>
                Feedlot Finishing
            </button>
            <button class="scenario-btn" onclick="loadScenario('acidosis')">
                <span class="scenario-label">Risk Analysis</span>
                Severe Acidosis
            </button>
            <button class="scenario-btn" onclick="loadScenario('starvation')">
                <span class="scenario-label">Deficiency</span>
                N-Starvation
            </button>
        </div>
    </div>

    <div class="main-grid">
        
        <!-- Feed Configuration -->
        <div class="config-panel">
            <div class="panel-header">Feed Configuration (kg DM/day)</div>
            
            <div class="feed-control">
                <div class="feed-label-row">
                    <span class="feed-name">Grass Hay</span>
                    <span class="feed-value" id="v_hay">0.0</span>
                </div>
                <div class="feed-meta">
                    <code>65% NDF</code> <code>6% CP</code> Slow digestion rate, requires nitrogen supplementation
                </div>
                <input type="range" id="hay" min="0" max="12" step="0.5" value="8" oninput="update()">
            </div>

            <div class="feed-control">
                <div class="feed-label-row">
                    <span class="feed-name">Alfalfa Hay</span>
                    <span class="feed-value" id="v_alf">0.0</span>
                </div>
                <div class="feed-meta">
                    <code>17% CP</code> High buffering capacity (Ca, K, Mg)
                </div>
                <input type="range" id="alf" min="0" max="8" step="0.5" value="0" oninput="update()">
            </div>

            <div class="feed-control">
                <div class="feed-label-row">
                    <span class="feed-name">Dry Rolled Corn</span>
                    <span class="feed-value" id="v_dry">0.0</span>
                </div>
                <div class="feed-meta">
                    <code>70% Starch</code> <code>K<sub>d</sub>=0.15</code> Moderate fermentation rate
                </div>
                <input type="range" id="dry" min="0" max="10" step="0.5" value="0" oninput="update()">
            </div>

            <div class="feed-control">
                <div class="feed-label-row">
                    <span class="feed-name">Steam Flaked Corn</span>
                    <span class="feed-value" id="v_wet">0.0</span>
                </div>
                <div class="feed-meta">
                    <code>75% Starch</code> <code>K<sub>d</sub>=0.40</code> Rapid acid production
                </div>
                <input type="range" id="wet" min="0" max="10" step="0.5" value="0" oninput="update()">
            </div>

            <div class="feed-control">
                <div class="feed-label-row">
                    <span class="feed-name">Soybean Meal</span>
                    <span class="feed-value" id="v_sbm">0.0</span>
                </div>
                <div class="feed-meta">
                    <code>48% CP</code> High RDP content, supports microbial growth
                </div>
                <input type="range" id="sbm" min="0" max="4" step="0.1" value="0" oninput="update()">
            </div>

            <div class="feed-control">
                <div class="feed-label-row">
                    <span class="feed-name">Fat/Oil Supplement</span>
                    <span class="feed-value" id="v_fat">0.0</span>
                </div>
                <div class="feed-meta">
                    <code>225% TDN</code> Microbial toxicity above 6-7% dietary inclusion
                </div>
                <input type="range" id="fat" min="0" max="1.5" step="0.1" value="0" oninput="update()">
            </div>
        </div>

        <!-- Metrics & Analysis -->
        <div class="metrics-section">
            
            <!-- Key Metrics -->
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Crude Protein</div>
                    <div class="metric-value" id="d_cp">0.0<span class="metric-unit">%</span></div>
                    <div class="metric-status status-optimal" id="s_cp">OPTIMAL</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Rumen pH</div>
                    <div class="metric-value" id="d_ph">0.00</div>
                    <div class="metric-status status-optimal" id="s_ph">OPTIMAL</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">peNDF</div>
                    <div class="metric-value" id="d_pendf">0<span class="metric-unit">%</span></div>
                    <div class="metric-status status-optimal" id="s_pendf">OPTIMAL</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Dietary Fat</div>
                    <div class="metric-value" id="d_fat">0.0<span class="metric-unit">%</span></div>
                    <div class="metric-status status-optimal" id="s_fat">OPTIMAL</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Starch</div>
                    <div class="metric-value" id="d_starch">0.0<span class="metric-unit">%</span></div>
                    <div class="metric-status status-optimal" id="s_starch">OPTIMAL</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Fiber Efficiency</div>
                    <div class="metric-value" id="d_efficiency">0<span class="metric-unit">%</span></div>
                    <div class="metric-status status-optimal" id="s_efficiency">OPTIMAL</div>
                </div>
            </div>
            
            <!-- Energy Chart -->
            <div class="chart-section">
                <div class="chart-header">Energy Utilization Analysis</div>
                <div class="chart-container">
                    <canvas id="mainChart"></canvas>
                </div>
            </div>
            
            <!-- Analysis Report -->
            <div class="analysis-section">
                <div class="analysis-header">Diagnostic Analysis</div>
                <div id="diagnostics">
                    <div style="text-align: center; padding: 40px; color: #9ca3af;">
                        Configure feed inputs to generate analysis
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Scientific References -->
    <div class="reference-section">
        <div class="reference-header">Scientific Framework</div>
        <div class="reference-content">
            <strong>Data Sources:</strong> Feed composition from NASEM (2016) Beef & Dairy Nutrient Requirements. 
            pH modeling adapted from Cornell Net Carbohydrate and Protein System (CNCPS). 
            Fermentation kinetics (K<sub>d</sub>) from Nocek & Tamminga (1991).
            <strong>Associative Effects:</strong> Nitrogen limitation effects (Klopfenstein 2001), 
            pH-mediated inhibition (Russell & Wilson 1996), fat toxicity mechanisms (Jenkins & Harvatine 2014), 
            passage rate dynamics (Allen 2000).
        </div>
    </div>

</div>

<script>
    const feeds = {
        hay: { cp: 6,   fat: 2.0, tdn: 52, ndf: 65, starch: 1,  peNDF: 55, fermentRate: 0.02 }, 
        alf: { cp: 17,  fat: 2.5, tdn: 58, ndf: 42, starch: 2,  peNDF: 35, fermentRate: 0.04 },  
        dry: { cp: 9,   fat: 4.0, tdn: 88, ndf: 9,  starch: 70, peNDF: 5,  fermentRate: 0.15 }, 
        wet: { cp: 9,   fat: 4.0, tdn: 92, ndf: 8,  starch: 75, peNDF: 2,  fermentRate: 0.40 },
        sbm: { cp: 48,  fat: 1.5, tdn: 84, ndf: 12, starch: 2,  peNDF: 0,  fermentRate: 0.10 }, 
        fat: { cp: 0,   fat: 100, tdn: 225,ndf: 0,  starch: 0,  peNDF: 0,  fermentRate: 0    } 
    };

    let chart;

    function loadScenario(type) {
        if(type === 'balanced') {
            setVals(5, 3, 3, 0, 1.0, 0);
        } else if(type === 'feedlot') {
            setVals(1.5, 0.5, 6, 2, 1.5, 0.3);
        } else if(type === 'acidosis') {
            setVals(1, 0, 0, 9, 0.3, 0);
        } else if(type === 'starvation') {
            setVals(10, 0, 0, 0, 0, 0);
        }
    }

    function setVals(h, a, d, w, s, f) {
        document.getElementById('hay').value = h;
        document.getElementById('alf').value = a;
        document.getElementById('dry').value = d;
        document.getElementById('wet').value = w;
        document.getElementById('sbm').value = s;
        document.getElementById('fat').value = f;
        update();
    }

    function update() {
        let h = +hay.value, a = +alf.value, d = +dry.value, w = +wet.value, s = +sbm.value, f = +fat.value;
        v_hay.innerText = h.toFixed(1); v_alf.innerText = a.toFixed(1); v_dry.innerText = d.toFixed(1);
        v_wet.innerText = w.toFixed(1); v_sbm.innerText = s.toFixed(1); v_fat.innerText = f.toFixed(1);

        let dm = h+a+d+w+s+f;
        if(dm <= 0) {
            document.getElementById('diagnostics').innerHTML = "<div style='text-align: center; padding: 40px; color: #9ca3af;'>Configure feed inputs to generate analysis</div>";
            if(chart) chart.destroy();
            return;
        }

        function chem(attr) {
            return ((h*feeds.hay[attr]) + (a*feeds.alf[attr]) + (d*feeds.dry[attr]) + 
                    (w*feeds.wet[attr]) + (s*feeds.sbm[attr]) + (f*feeds.fat[attr])) / dm;
        }

        let cp = chem('cp');
        let fat_pct = chem('fat');
        let ndf = chem('ndf');
        let starch = chem('starch');
        let peNDF = chem('peNDF');
        let avg_ferment = chem('fermentRate');
        let base_tdn = chem('tdn');

        // pH Model
        let base_ph = 6.8;
        let acid_load = starch * avg_ferment * 0.85; 
        let buffer_from_peNDF = peNDF * 0.014;
        let buffer_from_alfalfa = (a/dm) * 0.18;
        let total_buffer = buffer_from_peNDF + buffer_from_alfalfa;
        let ph = base_ph - acid_load + total_buffer;
        if(ph > 7.0) ph = 7.0;
        if(ph < 5.2) ph = 5.2;

        // Associative Effects
        let findings = [];
        let fiber_health = 1.0;
        let passage_loss = 0.0;

        // Nitrogen Limitation
        if(cp < 8.0) {
            let deficit = 8.0 - cp;
            let penalty = deficit * 0.17;
            fiber_health -= penalty;
            findings.push({
                type: 'critical',
                title: 'NITROGEN DEFICIENCY DETECTED',
                text: `Crude protein concentration of ${cp.toFixed(1)}% is below the minimum threshold of 8% required for microbial protein synthesis. Microbial population is nitrogen-limited, resulting in ${(penalty*100).toFixed(0)}% reduction in fiber digestion efficiency. Recommend immediate protein supplementation.`
            });
        } else if(cp < 10.0) {
            findings.push({
                type: 'warning',
                title: 'Suboptimal Protein Levels',
                text: `Current CP level of ${cp.toFixed(1)}% meets minimum requirements but falls below optimal range (10-13%) for high-producing animals. Consider increased protein supplementation for maximum performance.`
            });
        } else {
            if(h > 4 && s > 0.5) {
                findings.push({
                    type: 'info',
                    title: 'Positive Associative Effect',
                    text: `Protein supplementation is successfully enhancing low-quality forage utilization. This demonstrates beneficial synergy between protein supplements and fibrous feedstuffs.`
                });
            } else {
                findings.push({
                    type: 'optimal',
                    title: 'Adequate Nitrogen Status',
                    text: `Crude protein level of ${cp.toFixed(1)}% is sufficient to support optimal microbial protein synthesis and fiber fermentation.`
                });
            }
        }

        // pH / Acidosis
        if(ph < 5.8) {
            let severity = 6.0 - ph;
            let penalty = severity * 1.0;
            if(penalty > 0.85) penalty = 0.85;
            fiber_health -= penalty;
            findings.push({
                type: 'critical',
                title: 'ACUTE RUMINAL ACIDOSIS',
                text: `Rumen pH of ${ph.toFixed(2)} indicates severe acidotic conditions. Cellulolytic bacteria populations are critically suppressed, resulting in ${(penalty*100).toFixed(0)}% loss of fiber digestion capacity. Risk of laminitis, reduced intake, and metabolic disorders. Immediate intervention required: reduce rapidly fermentable carbohydrates and increase effective fiber.`
            });
        } else if(ph < 6.0) {
            let severity = 6.0 - ph;
            let penalty = severity * 0.75;
            fiber_health -= penalty;
            findings.push({
                type: 'critical',
                title: 'SUBACUTE RUMINAL ACIDOSIS (SARA)',
                text: `pH of ${ph.toFixed(2)} is within SARA range. Fiber-digesting bacteria are significantly inhibited (${(penalty*100).toFixed(0)}% efficiency loss). Clinical signs may include reduced feed intake, inconsistent manure, and decreased milk fat or weight gains. Adjust ration to increase buffering capacity.`
            });
        } else if(ph < 6.2) {
            let mild = 6.2 - ph;
            let penalty = mild * 0.40;
            fiber_health -= penalty;
            findings.push({
                type: 'warning',
                title: 'pH Suboptimal',
                text: `Rumen pH of ${ph.toFixed(2)} is below optimal range. Cellulolytic bacterial activity is beginning to decline (${(penalty*100).toFixed(0)}% reduction). Monitor for early signs of acidosis and consider increasing effective fiber or buffering agents.`
            });
        } else if(ph < 6.4) {
            findings.push({
                type: 'optimal',
                title: 'Acceptable pH Range',
                text: `Current pH of ${ph.toFixed(2)} is within acceptable functional range, though not optimal. Fiber fermentation is proceeding normally.`
            });
        } else {
            findings.push({
                type: 'optimal',
                title: 'Optimal pH Status',
                text: `Rumen pH of ${ph.toFixed(2)} is in the ideal range (6.4-7.0) for cellulolytic bacteria. Fiber fermentation efficiency is maximized.`
            });
        }

        // Fat Toxicity
        if(fat_pct > 7.0) {
            let excess = fat_pct - 7.0;
            let penalty = excess * 0.13;
            if(penalty > 0.55) penalty = 0.55;
            fiber_health -= penalty;
            findings.push({
                type: 'critical',
                title: 'DIETARY FAT TOXICITY',
                text: `Fat concentration of ${fat_pct.toFixed(1)}% exceeds the recommended maximum of 6-7% of dietary dry matter. Excessive fat physically coats feed particles and exhibits direct antimicrobial effects on gram-positive bacteria, reducing fiber digestion by ${(penalty*100).toFixed(0)}%. Reduce fat supplementation immediately.`
            });
        } else if(fat_pct > 6.0) {
            let mild_excess = fat_pct - 6.0;
            let penalty = mild_excess * 0.09;
            fiber_health -= penalty;
            findings.push({
                type: 'warning',
                title: 'Elevated Fat Levels',
                text: `Dietary fat at ${fat_pct.toFixed(1)}% is approaching upper safety threshold. Monitor for signs of depressed fiber digestion and reduced dry matter intake. Consider limiting further fat supplementation.`
            });
        } else {
            findings.push({
                type: 'optimal',
                title: 'Safe Fat Concentration',
                text: `Dietary fat level of ${fat_pct.toFixed(1)}% is within safe limits for normal rumen function.`
            });
        }

        // Passage Rate
        if(peNDF < 15) {
            passage_loss = (20 - peNDF) * 0.015;
            if(passage_loss > 0.20) passage_loss = 0.20;
            findings.push({
                type: 'critical',
                title: 'INADEQUATE EFFECTIVE FIBER',
                text: `Physical effective NDF of ${peNDF.toFixed(1)}% is severely deficient (target: 18-22%). Insufficient rumination reduces retention time, causing premature passage of feed particles before complete fermentation. Energy loss: ${(passage_loss*100).toFixed(0)}%. Increase forage particle size and inclusion rate.`
            });
        } else if(peNDF < 20) {
            passage_loss = (20 - peNDF) * 0.012;
            findings.push({
                type: 'warning',
                title: 'Below-Target Effective Fiber',
                text: `peNDF of ${peNDF.toFixed(1)}% is below recommended range. Reduced chewing activity may lead to increased passage rates and incomplete digestion (${(passage_loss*100).toFixed(0)}% energy loss). Consider increasing long-stem forage.`
            });
        } else if(peNDF > 35) {
            findings.push({
                type: 'optimal',
                title: 'High Fiber Mat Formation',
                text: `peNDF of ${peNDF.toFixed(1)}% promotes excellent rumen health and optimal retention time. Note: very high fiber diets may limit dry matter intake in high-producing animals.`
            });
        } else {
            findings.push({
                type: 'optimal',
                title: 'Optimal Effective Fiber',
                text: `peNDF of ${peNDF.toFixed(1)}% provides adequate rumination stimulus and appropriate feed retention time for complete fermentation.`
            });
        }

        if(fiber_health < 0) fiber_health = 0;
        if(fiber_health > 1) fiber_health = 1;

        // Energy Partitioning
        let fiber_tdn_potential = (h * feeds.hay.tdn) + (a * feeds.alf.tdn);
        let nonfiber_tdn_potential = (d * feeds.dry.tdn) + (w * feeds.wet.tdn) + 
                                      (s * feeds.sbm.tdn) + (f * feeds.fat.tdn);
        
        let net_fiber_efficiency = fiber_health - passage_loss;
        if(net_fiber_efficiency < 0) net_fiber_efficiency = 0;
        let captured_fiber = fiber_tdn_potential * net_fiber_efficiency;
        
        let nonfiber_efficiency = 1.0;
        if(ph < 5.5) {
            nonfiber_efficiency = 0.90;
            findings.push({
                type: 'warning',
                title: 'Epithelial Damage',
                text: `Extreme acidosis (pH < 5.5) is causing rumen epithelial damage and reduced nutrient absorption capacity. Even non-fiber energy sources are being underutilized.`
            });
        } else if(ph < 5.8) {
            nonfiber_efficiency = 0.96;
        }
        let captured_nonfiber = nonfiber_tdn_potential * nonfiber_efficiency;
        
        let total_potential = fiber_tdn_potential + nonfiber_tdn_potential;
        let total_realized = captured_fiber + captured_nonfiber;
        let total_waste = total_potential - total_realized;

        // Update Metrics
        d_cp.innerHTML = cp.toFixed(1) + '<span class="metric-unit">%</span>';
        d_ph.innerText = ph.toFixed(2);
        d_pendf.innerHTML = peNDF.toFixed(0) + '<span class="metric-unit">%</span>';
        d_fat.innerHTML = fat_pct.toFixed(1) + '<span class="metric-unit">%</span>';
        d_starch.innerHTML = starch.toFixed(1) + '<span class="metric-unit">%</span>';
        d_efficiency.innerHTML = (fiber_health*100).toFixed(0) + '<span class="metric-unit">%</span>';

        // Status Indicators
        updateStatus('s_cp', cp, 10, 8, 'CP');
        updateStatus('s_ph', ph, 6.4, 6.0, 'pH');
        updateStatus('s_pendf', peNDF, 20, 15, 'peNDF');
        updateStatus('s_fat', fat_pct, 6, 7, 'fat', true);
        updateStatus('s_starch', starch, 30, 40, 'starch');
        updateStatus('s_efficiency', fiber_health*100, 85, 70, 'efficiency');

        // Generate Report
        let efficiency_pct = (total_realized / total_potential * 100).toFixed(1);
        let summary = `
            <div class="summary-panel">
                <div class="summary-row">
                    <span class="summary-label">Total Dry Matter Intake:</span>
                    <span class="summary-value">${dm.toFixed(1)} kg/day</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Potential Energy:</span>
                    <span class="summary-value">${total_potential.toFixed(1)} kg TDN</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Captured Energy:</span>
                    <span class="summary-value">${total_realized.toFixed(1)} kg TDN</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">System Efficiency:</span>
                    <span class="summary-value">${efficiency_pct}%</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Energy Loss:</span>
                    <span class="summary-value" style="color: #dc2626;">${total_waste.toFixed(1)} kg TDN</span>
                </div>
            </div>
            <div class="findings-list">
                ${findings.map(f => `
                    <div class="finding finding-${f.type}">
                        <span class="finding-title">${f.title}</span>
                        ${f.text}
                    </div>
                `).join('')}
            </div>
        `;

        document.getElementById('diagnostics').innerHTML = summary;
        updateChart(captured_fiber, captured_nonfiber, total_waste);
    }

    function updateStatus(id, value, optimal, warning, type, inverse = false) {
        let el = document.getElementById(id);
        let status, text;
        
        if(type === 'pH') {
            if(value >= 6.4) { status = 'optimal'; text = 'OPTIMAL'; }
            else if(value >= 6.0) { status = 'warning'; text = 'CAUTION'; }
            else { status = 'critical'; text = 'CRITICAL'; }
        } else if(inverse) {
            if(value <= optimal) { status = 'optimal'; text = 'OPTIMAL'; }
            else if(value <= warning) { status = 'warning'; text = 'ELEVATED'; }
            else { status = 'critical'; text = 'EXCESSIVE'; }
        } else {
            if(value >= optimal) { status = 'optimal'; text = 'OPTIMAL'; }
            else if(value >= warning) { status = 'warning'; text = 'SUBOPTIMAL'; }
            else { status = 'critical'; text = 'DEFICIENT'; }
        }
        
        el.className = 'metric-status status-' + status;
        el.innerText = text;
    }

    function updateChart(fib, other, waste) {
        const ctx = document.getElementById('mainChart').getContext('2d');
        if(chart) chart.destroy();
        
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Total Digestible Nutrients (kg/day)'],
                datasets: [
                    { 
                        label: 'Fiber Energy (Captured)', 
                        data: [fib], 
                        backgroundColor: '#10b981',
                        stack: 'Stack 0'
                    },
                    { 
                        label: 'Non-Fiber Energy (Captured)', 
                        data: [other], 
                        backgroundColor: '#3b82f6',
                        stack: 'Stack 0'
                    },
                    { 
                        label: 'Lost to Inhibition/Passage', 
                        data: [waste], 
                        backgroundColor: '#ef4444',
                        stack: 'Stack 0'
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: { 
                    x: { 
                        stacked: true, 
                        beginAtZero: true,
                        title: { 
                            display: true, 
                            text: 'Total Digestible Nutrients (kg/day)',
                            font: { size: 12, weight: '600' }
                        },
                        grid: { color: '#f3f4f6' }
                    }, 
                    y: { 
                        stacked: true,
                        grid: { display: false }
                    } 
                },
                plugins: {
                    legend: { 
                        position: 'bottom',
                        labels: { 
                            boxWidth: 12, 
                            padding: 15,
                            font: { size: 11 }
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1f2937',
                        titleFont: { size: 13, weight: '600' },
                        bodyFont: { size: 12 },
                        padding: 12,
                        displayColors: true,
                        boxWidth: 10,
                        boxHeight: 10
                    }
                }
            }
        });
    }

    setTimeout(() => loadScenario('balanced'), 100);
</script>
</body>
</html>
"""
    
    filename = "rumen_professional.html"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ Professional Rumen Optimization Platform created!")
    print("\n📊 Enterprise Features:")
    print("  • Corporate navigation bar")
    print("  • Professional color scheme (blue/gray)")
    print("  • Scientific terminology")
    print("  • Business dashboard layout")
    print("  • Metric status indicators")
    print("  • Formal findings report")
    print("  • Clean typography (system fonts)")
    print("  • Minimalist design language")
    print("\n🎯 Professional Enhancements:")
    print("  • No emoji icons")
    print("  • Technical language throughout")
    print("  • Status badges (OPTIMAL/CAUTION/CRITICAL)")
    print("  • Structured diagnostic reports")
    print("  • Scientific reference citations")
    
    webbrowser.open('file://' + os.path.realpath(filename))

if __name__ == "__main__":
    create_professional_rumen_simulation()