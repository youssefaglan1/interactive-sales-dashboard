# ============================================================
#  Sales Performance Dashboard — Generator
#  Run:  python sales_dashboard.py
#  Opens the dashboard automatically in your browser
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sales Performance Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
  :root {
    --bg: #0a0e1a; --surface: #111827; --surface2: #1a2235; --border: #1e2d45;
    --accent: #3b82f6; --accent2: #06b6d4; --accent3: #8b5cf6;
    --green: #10b981; --amber: #f59e0b; --red: #ef4444;
    --text: #f1f5f9; --muted: #64748b;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'DM Sans', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; padding: 24px; }
  .header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 28px; flex-wrap: wrap; gap: 16px; }
  .header-left h1 { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #f1f5f9, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px; }
  .header-left p { color: var(--muted); font-size: 13px; margin-top: 4px; }
  .last-updated { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 8px 14px; font-size: 12px; color: var(--muted); }
  .dot { width: 7px; height: 7px; background: var(--green); border-radius: 50%; display: inline-block; margin-right: 6px; animation: pulse 2s infinite; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
  .filters-bar { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 16px 20px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; margin-bottom: 24px; }
  .filters-bar label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 500; }
  .filter-group { display: flex; flex-direction: column; gap: 5px; }
  select, input[type="date"] { background: var(--surface2); border: 1px solid var(--border); color: var(--text); font-family: 'DM Sans', sans-serif; font-size: 13px; padding: 7px 12px; border-radius: 8px; outline: none; cursor: pointer; min-width: 130px; transition: border-color 0.2s; }
  select:hover, input[type="date"]:hover { border-color: var(--accent); }
  .filter-divider { width: 1px; height: 40px; background: var(--border); }
  .reset-btn { margin-left: auto; background: var(--accent); color: white; border: none; padding: 8px 18px; border-radius: 8px; font-size: 13px; font-family: 'DM Sans', sans-serif; cursor: pointer; font-weight: 500; transition: opacity 0.2s; }
  .reset-btn:hover { opacity: 0.85; }
  .kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
  .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 22px 24px; position: relative; overflow: hidden; transition: transform 0.2s, border-color 0.2s; }
  .kpi-card:hover { transform: translateY(-2px); border-color: var(--accent); }
  .kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }
  .kpi-card.revenue::before { background: linear-gradient(90deg, var(--accent), var(--accent2)); }
  .kpi-card.profit::before { background: linear-gradient(90deg, var(--green), #34d399); }
  .kpi-card.orders::before { background: linear-gradient(90deg, var(--accent3), #a78bfa); }
  .kpi-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-bottom: 14px; }
  .kpi-card.revenue .kpi-icon { background: rgba(59,130,246,0.15); }
  .kpi-card.profit .kpi-icon { background: rgba(16,185,129,0.15); }
  .kpi-card.orders .kpi-icon { background: rgba(139,92,246,0.15); }
  .kpi-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.8px; font-weight: 500; margin-bottom: 6px; }
  .kpi-value { font-family: 'Syne', sans-serif; font-size: 30px; font-weight: 800; line-height: 1; }
  .kpi-card.revenue .kpi-value { color: var(--accent); }
  .kpi-card.profit .kpi-value { color: var(--green); }
  .kpi-card.orders .kpi-value { color: var(--accent3); }
  .kpi-sub { font-size: 12px; color: var(--muted); margin-top: 6px; }
  .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
  .chart-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 22px 24px; }
  .chart-card.full { grid-column: 1 / -1; }
  .chart-title { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; margin-bottom: 4px; color: var(--text); }
  .chart-subtitle { font-size: 11px; color: var(--muted); margin-bottom: 18px; }
  .chart-container { position: relative; }
  .insights-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 22px 24px; margin-bottom: 16px; }
  .insights-title { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
  .insights-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .insight-item { background: var(--surface2); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; }
  .insight-icon { font-size: 20px; margin-bottom: 8px; }
  .insight-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.7px; margin-bottom: 4px; }
  .insight-value { font-size: 14px; font-weight: 600; color: var(--text); }
  .insight-desc { font-size: 11px; color: var(--muted); margin-top: 3px; }
  .table-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 22px 24px; overflow: hidden; }
  .table-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { color: var(--muted); font-size: 10px; text-transform: uppercase; letter-spacing: 0.7px; font-weight: 500; padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--border); }
  td { padding: 10px 12px; border-bottom: 1px solid rgba(30,45,69,0.5); }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: var(--surface2); }
  .cat-badge { padding: 2px 8px; border-radius: 20px; font-size: 11px; font-weight: 500; }
  .cat-electronics { background: rgba(59,130,246,0.15); color: #60a5fa; }
  .cat-furniture { background: rgba(245,158,11,0.15); color: #fbbf24; }
  @media (max-width: 900px) { .charts-grid { grid-template-columns: 1fr; } .kpi-grid { grid-template-columns: 1fr; } .insights-grid { grid-template-columns: 1fr 1fr; } }
</style>
</head>
<body>
<div class="header">
  <div class="header-left">
    <h1>📊 Sales Performance Dashboard</h1>
    <p>Q1 2024 · Egypt Region · 100 Orders Analyzed</p>
  </div>
  <div class="last-updated"><span class="dot"></span>Data Period: Jan–Mar 2024</div>
</div>
<div class="filters-bar">
  <div class="filter-group"><label>From Date</label><input type="date" id="dateFrom" value="2024-01-01"></div>
  <div class="filter-group"><label>To Date</label><input type="date" id="dateTo" value="2024-03-31"></div>
  <div class="filter-divider"></div>
  <div class="filter-group"><label>Category</label>
    <select id="catFilter"><option value="all">All Categories</option><option value="Electronics">Electronics</option><option value="Furniture">Furniture</option></select>
  </div>
  <div class="filter-group"><label>Region</label>
    <select id="regionFilter"><option value="all">All Regions</option><option value="Alexandria">Alexandria</option><option value="Cairo">Cairo</option><option value="Tanta">Tanta</option><option value="Suez">Suez</option><option value="Giza">Giza</option><option value="Mansoura">Mansoura</option></select>
  </div>
  <div class="filter-group"><label>Product</label>
    <select id="productFilter"><option value="all">All Products</option><option value="Phone">Phone</option><option value="Monitor">Monitor</option><option value="Laptop">Laptop</option><option value="Desk">Desk</option><option value="Table">Table</option><option value="Chair">Chair</option><option value="Headphones">Headphones</option></select>
  </div>
  <button class="reset-btn" onclick="resetFilters()">↺ Reset</button>
</div>
<div class="kpi-grid">
  <div class="kpi-card revenue"><div class="kpi-icon">💰</div><div class="kpi-label">Total Revenue</div><div class="kpi-value" id="kpiRevenue">$0</div><div class="kpi-sub" id="kpiRevSub">—</div></div>
  <div class="kpi-card profit"><div class="kpi-icon">📈</div><div class="kpi-label">Total Profit</div><div class="kpi-value" id="kpiProfit">$0</div><div class="kpi-sub" id="kpiProfSub">—</div></div>
  <div class="kpi-card orders"><div class="kpi-icon">🛒</div><div class="kpi-label">Total Orders</div><div class="kpi-value" id="kpiOrders">0</div><div class="kpi-sub" id="kpiOrdSub">—</div></div>
</div>
<div class="charts-grid">
  <div class="chart-card full"><div class="chart-title">Revenue Over Time</div><div class="chart-subtitle">Monthly revenue trend across the selected period</div><div class="chart-container" style="height:220px"><canvas id="lineChart"></canvas></div></div>
</div>
<div class="charts-grid">
  <div class="chart-card"><div class="chart-title">Revenue by Product</div><div class="chart-subtitle">Top performing products by total revenue</div><div class="chart-container" style="height:240px"><canvas id="productBar"></canvas></div></div>
  <div class="chart-card"><div class="chart-title">Revenue by Category</div><div class="chart-subtitle">Electronics vs Furniture distribution</div><div class="chart-container" style="height:240px"><canvas id="pieChart"></canvas></div></div>
</div>
<div class="charts-grid">
  <div class="chart-card"><div class="chart-title">Revenue by Region</div><div class="chart-subtitle">Geographic sales performance</div><div class="chart-container" style="height:240px"><canvas id="regionBar"></canvas></div></div>
  <div class="chart-card"><div class="chart-title">Profit by Product</div><div class="chart-subtitle">Net profit contribution per product</div><div class="chart-container" style="height:240px"><canvas id="profitBar"></canvas></div></div>
</div>
<div class="insights-card">
  <div class="insights-title">💡 Key Business Insights</div>
  <div class="insights-grid">
    <div class="insight-item"><div class="insight-icon">🏆</div><div class="insight-label">Top Product</div><div class="insight-value" id="insTopProd">—</div><div class="insight-desc" id="insTopProdSub">—</div></div>
    <div class="insight-item"><div class="insight-icon">📍</div><div class="insight-label">Best Region</div><div class="insight-value" id="insBestRegion">—</div><div class="insight-desc" id="insBestRegionSub">—</div></div>
    <div class="insight-item"><div class="insight-icon">📅</div><div class="insight-label">Best Month</div><div class="insight-value" id="insBestMonth">—</div><div class="insight-desc" id="insBestMonthSub">—</div></div>
    <div class="insight-item"><div class="insight-icon">💹</div><div class="insight-label">Profit Margin</div><div class="insight-value" id="insMargin">—</div><div class="insight-desc" id="insMarginSub">—</div></div>
  </div>
</div>
<div class="table-card">
  <div class="table-header"><div><div class="chart-title">Top 10 Orders by Revenue</div><div class="chart-subtitle">Highest revenue transactions in selected filter</div></div></div>
  <table><thead><tr><th>Order ID</th><th>Date</th><th>Product</th><th>Category</th><th>Region</th><th>Qty</th><th>Revenue</th><th>Profit</th></tr></thead><tbody id="topOrdersBody"></tbody></table>
</div>
<script>
const RAW = [{"order_id":1001,"date":"2024-01-05","ym":"2024-01","product":"Table","category":"Furniture","quantity":4,"unit_price":350,"cost":220,"region":"Mansoura","revenue":1400,"total_cost":880,"profit":520},{"order_id":1002,"date":"2024-03-28","ym":"2024-03","product":"Laptop","category":"Electronics","quantity":2,"unit_price":1200,"cost":900,"region":"Suez","revenue":2400,"total_cost":1800,"profit":600},{"order_id":1003,"date":"2024-03-08","ym":"2024-03","product":"Desk","category":"Furniture","quantity":4,"unit_price":300,"cost":200,"region":"Mansoura","revenue":1200,"total_cost":800,"profit":400},{"order_id":1004,"date":"2024-01-07","ym":"2024-01","product":"Monitor","category":"Electronics","quantity":4,"unit_price":400,"cost":250,"region":"Cairo","revenue":1600,"total_cost":1000,"profit":600},{"order_id":1005,"date":"2024-01-21","ym":"2024-01","product":"Table","category":"Furniture","quantity":5,"unit_price":350,"cost":220,"region":"Suez","revenue":1750,"total_cost":1100,"profit":650},{"order_id":1006,"date":"2024-02-21","ym":"2024-02","product":"Headphones","category":"Electronics","quantity":5,"unit_price":100,"cost":60,"region":"Alexandria","revenue":500,"total_cost":300,"profit":200},{"order_id":1007,"date":"2024-02-04","ym":"2024-02","product":"Desk","category":"Furniture","quantity":4,"unit_price":300,"cost":200,"region":"Alexandria","revenue":1200,"total_cost":800,"profit":400},{"order_id":1008,"date":"2024-01-13","ym":"2024-01","product":"Desk","category":"Furniture","quantity":2,"unit_price":300,"cost":200,"region":"Alexandria","revenue":600,"total_cost":400,"profit":200},{"order_id":1009,"date":"2024-01-18","ym":"2024-01","product":"Laptop","category":"Electronics","quantity":4,"unit_price":1200,"cost":900,"region":"Tanta","revenue":4800,"total_cost":3600,"profit":1200},{"order_id":1010,"date":"2024-02-26","ym":"2024-02","product":"Desk","category":"Furniture","quantity":4,"unit_price":300,"cost":200,"region":"Tanta","revenue":1200,"total_cost":800,"profit":400},{"order_id":1011,"date":"2024-03-10","ym":"2024-03","product":"Table","category":"Furniture","quantity":3,"unit_price":350,"cost":220,"region":"Mansoura","revenue":1050,"total_cost":660,"profit":390},{"order_id":1012,"date":"2024-03-20","ym":"2024-03","product":"Table","category":"Furniture","quantity":1,"unit_price":350,"cost":220,"region":"Alexandria","revenue":350,"total_cost":220,"profit":130},{"order_id":1013,"date":"2024-03-23","ym":"2024-03","product":"Desk","category":"Furniture","quantity":3,"unit_price":300,"cost":200,"region":"Suez","revenue":900,"total_cost":600,"profit":300},{"order_id":1014,"date":"2024-03-13","ym":"2024-03","product":"Chair","category":"Furniture","quantity":1,"unit_price":150,"cost":90,"region":"Mansoura","revenue":150,"total_cost":90,"profit":60},{"order_id":1015,"date":"2024-01-06","ym":"2024-01","product":"Table","category":"Furniture","quantity":3,"unit_price":350,"cost":220,"region":"Cairo","revenue":1050,"total_cost":660,"profit":390},{"order_id":1016,"date":"2024-02-05","ym":"2024-02","product":"Monitor","category":"Electronics","quantity":4,"unit_price":400,"cost":250,"region":"Giza","revenue":1600,"total_cost":1000,"profit":600},{"order_id":1017,"date":"2024-03-18","ym":"2024-03","product":"Monitor","category":"Electronics","quantity":4,"unit_price":400,"cost":250,"region":"Mansoura","revenue":1600,"total_cost":1000,"profit":600},{"order_id":1018,"date":"2024-01-29","ym":"2024-01","product":"Headphones","category":"Electronics","quantity":4,"unit_price":100,"cost":60,"region":"Giza","revenue":400,"total_cost":240,"profit":160},{"order_id":1019,"date":"2024-03-10","ym":"2024-03","product":"Monitor","category":"Electronics","quantity":4,"unit_price":400,"cost":250,"region":"Alexandria","revenue":1600,"total_cost":1000,"profit":600},{"order_id":1020,"date":"2024-01-24","ym":"2024-01","product":"Phone","category":"Electronics","quantity":1,"unit_price":600,"cost":400,"region":"Giza","revenue":600,"total_cost":400,"profit":200},{"order_id":1021,"date":"2024-03-09","ym":"2024-03","product":"Monitor","category":"Electronics","quantity":2,"unit_price":400,"cost":250,"region":"Tanta","revenue":800,"total_cost":500,"profit":300},{"order_id":1022,"date":"2024-01-13","ym":"2024-01","product":"Desk","category":"Furniture","quantity":5,"unit_price":300,"cost":200,"region":"Mansoura","revenue":1500,"total_cost":1000,"profit":500},{"order_id":1023,"date":"2024-03-02","ym":"2024-03","product":"Desk","category":"Furniture","quantity":1,"unit_price":300,"cost":200,"region":"Alexandria","revenue":300,"total_cost":200,"profit":100},{"order_id":1024,"date":"2024-02-22","ym":"2024-02","product":"Table","category":"Furniture","quantity":2,"unit_price":350,"cost":220,"region":"Tanta","revenue":700,"total_cost":440,"profit":260},{"order_id":1025,"date":"2024-01-13","ym":"2024-01","product":"Laptop","category":"Electronics","quantity":5,"unit_price":1200,"cost":900,"region":"Alexandria","revenue":6000,"total_cost":4500,"profit":1500},{"order_id":1026,"date":"2024-03-08","ym":"2024-03","product":"Table","category":"Furniture","quantity":2,"unit_price":350,"cost":220,"region":"Suez","revenue":700,"total_cost":440,"profit":260},{"order_id":1027,"date":"2024-01-28","ym":"2024-01","product":"Monitor","category":"Electronics","quantity":3,"unit_price":400,"cost":250,"region":"Suez","revenue":1200,"total_cost":750,"profit":450},{"order_id":1028,"date":"2024-01-08","ym":"2024-01","product":"Headphones","category":"Electronics","quantity":4,"unit_price":100,"cost":60,"region":"Suez","revenue":400,"total_cost":240,"profit":160},{"order_id":1029,"date":"2024-03-13","ym":"2024-03","product":"Monitor","category":"Electronics","quantity":3,"unit_price":400,"cost":250,"region":"Tanta","revenue":1200,"total_cost":750,"profit":450},{"order_id":1030,"date":"2024-02-26","ym":"2024-02","product":"Monitor","category":"Electronics","quantity":1,"unit_price":400,"cost":250,"region":"Cairo","revenue":400,"total_cost":250,"profit":150},{"order_id":1031,"date":"2024-03-22","ym":"2024-03","product":"Monitor","category":"Electronics","quantity":1,"unit_price":400,"cost":250,"region":"Cairo","revenue":400,"total_cost":250,"profit":150},{"order_id":1032,"date":"2024-01-14","ym":"2024-01","product":"Desk","category":"Furniture","quantity":2,"unit_price":300,"cost":200,"region":"Cairo","revenue":600,"total_cost":400,"profit":200},{"order_id":1033,"date":"2024-02-27","ym":"2024-02","product":"Desk","category":"Furniture","quantity":3,"unit_price":300,"cost":200,"region":"Suez","revenue":900,"total_cost":600,"profit":300},{"order_id":1034,"date":"2024-03-24","ym":"2024-03","product":"Monitor","category":"Electronics","quantity":4,"unit_price":400,"cost":250,"region":"Cairo","revenue":1600,"total_cost":1000,"profit":600},{"order_id":1035,"date":"2024-03-07","ym":"2024-03","product":"Desk","category":"Furniture","quantity":2,"unit_price":300,"cost":200,"region":"Mansoura","revenue":600,"total_cost":400,"profit":200},{"order_id":1036,"date":"2024-01-22","ym":"2024-01","product":"Desk","category":"Furniture","quantity":2,"unit_price":300,"cost":200,"region":"Suez","revenue":600,"total_cost":400,"profit":200},{"order_id":1037,"date":"2024-01-22","ym":"2024-01","product":"Headphones","category":"Electronics","quantity":1,"unit_price":100,"cost":60,"region":"Giza","revenue":100,"total_cost":60,"profit":40},{"order_id":1038,"date":"2024-02-21","ym":"2024-02","product":"Phone","category":"Electronics","quantity":2,"unit_price":600,"cost":400,"region":"Cairo","revenue":1200,"total_cost":800,"profit":400},{"order_id":1039,"date":"2024-03-03","ym":"2024-03","product":"Chair","category":"Furniture","quantity":1,"unit_price":150,"cost":90,"region":"Tanta","revenue":150,"total_cost":90,"profit":60},{"order_id":1040,"date":"2024-01-25","ym":"2024-01","product":"Table","category":"Furniture","quantity":1,"unit_price":350,"cost":220,"region":"Alexandria","revenue":350,"total_cost":220,"profit":130},{"order_id":1041,"date":"2024-03-18","ym":"2024-03","product":"Monitor","category":"Electronics","quantity":1,"unit_price":400,"cost":250,"region":"Giza","revenue":400,"total_cost":250,"profit":150},{"order_id":1042,"date":"2024-02-01","ym":"2024-02","product":"Headphones","category":"Electronics","quantity":5,"unit_price":100,"cost":60,"region":"Giza","revenue":500,"total_cost":300,"profit":200},{"order_id":1043,"date":"2024-02-27","ym":"2024-02","product":"Monitor","category":"Electronics","quantity":2,"unit_price":400,"cost":250,"region":"Alexandria","revenue":800,"total_cost":500,"profit":300},{"order_id":1044,"date":"2024-02-15","ym":"2024-02","product":"Chair","category":"Furniture","quantity":3,"unit_price":150,"cost":90,"region":"Suez","revenue":450,"total_cost":270,"profit":180},{"order_id":1045,"date":"2024-02-03","ym":"2024-02","product":"Desk","category":"Furniture","quantity":1,"unit_price":300,"cost":200,"region":"Cairo","revenue":300,"total_cost":200,"profit":100},{"order_id":1046,"date":"2024-01-18","ym":"2024-01","product":"Table","category":"Furniture","quantity":3,"unit_price":350,"cost":220,"region":"Tanta","revenue":1050,"total_cost":660,"profit":390},{"order_id":1047,"date":"2024-02-27","ym":"2024-02","product":"Headphones","category":"Electronics","quantity":3,"unit_price":100,"cost":60,"region":"Alexandria","revenue":300,"total_cost":180,"profit":120},{"order_id":1048,"date":"2024-03-07","ym":"2024-03","product":"Chair","category":"Furniture","quantity":2,"unit_price":150,"cost":90,"region":"Alexandria","revenue":300,"total_cost":180,"profit":120},{"order_id":1049,"date":"2024-01-12","ym":"2024-01","product":"Laptop","category":"Electronics","quantity":1,"unit_price":1200,"cost":900,"region":"Alexandria","revenue":1200,"total_cost":900,"profit":300},{"order_id":1050,"date":"2024-02-19","ym":"2024-02","product":"Desk","category":"Furniture","quantity":3,"unit_price":300,"cost":200,"region":"Tanta","revenue":900,"total_cost":600,"profit":300},{"order_id":1051,"date":"2024-03-24","ym":"2024-03","product":"Laptop","category":"Electronics","quantity":1,"unit_price":1200,"cost":900,"region":"Tanta","revenue":1200,"total_cost":900,"profit":300},{"order_id":1052,"date":"2024-03-12","ym":"2024-03","product":"Phone","category":"Electronics","quantity":5,"unit_price":600,"cost":400,"region":"Alexandria","revenue":3000,"total_cost":2000,"profit":1000},{"order_id":1053,"date":"2024-01-21","ym":"2024-01","product":"Desk","category":"Furniture","quantity":5,"unit_price":300,"cost":200,"region":"Tanta","revenue":1500,"total_cost":1000,"profit":500},{"order_id":1054,"date":"2024-01-11","ym":"2024-01","product":"Monitor","category":"Electronics","quantity":5,"unit_price":400,"cost":250,"region":"Giza","revenue":2000,"total_cost":1250,"profit":750},{"order_id":1055,"date":"2024-02-23","ym":"2024-02","product":"Table","category":"Furniture","quantity":4,"unit_price":350,"cost":220,"region":"Tanta","revenue":1400,"total_cost":880,"profit":520},{"order_id":1056,"date":"2024-03-18","ym":"2024-03","product":"Table","category":"Furniture","quantity":4,"unit_price":350,"cost":220,"region":"Alexandria","revenue":1400,"total_cost":880,"profit":520},{"order_id":1057,"date":"2024-02-16","ym":"2024-02","product":"Laptop","category":"Electronics","quantity":1,"unit_price":1200,"cost":900,"region":"Cairo","revenue":1200,"total_cost":900,"profit":300},{"order_id":1058,"date":"2024-03-21","ym":"2024-03","product":"Desk","category":"Furniture","quantity":3,"unit_price":300,"cost":200,"region":"Alexandria","revenue":900,"total_cost":600,"profit":300},{"order_id":1059,"date":"2024-01-10","ym":"2024-01","product":"Headphones","category":"Electronics","quantity":2,"unit_price":100,"cost":60,"region":"Mansoura","revenue":200,"total_cost":120,"profit":80},{"order_id":1060,"date":"2024-02-24","ym":"2024-02","product":"Phone","category":"Electronics","quantity":4,"unit_price":600,"cost":400,"region":"Tanta","revenue":2400,"total_cost":1600,"profit":800},{"order_id":1061,"date":"2024-03-04","ym":"2024-03","product":"Phone","category":"Electronics","quantity":1,"unit_price":600,"cost":400,"region":"Tanta","revenue":600,"total_cost":400,"profit":200},{"order_id":1062,"date":"2024-01-18","ym":"2024-01","product":"Chair","category":"Furniture","quantity":1,"unit_price":150,"cost":90,"region":"Cairo","revenue":150,"total_cost":90,"profit":60},{"order_id":1063,"date":"2024-03-22","ym":"2024-03","product":"Headphones","category":"Electronics","quantity":2,"unit_price":100,"cost":60,"region":"Alexandria","revenue":200,"total_cost":120,"profit":80},{"order_id":1064,"date":"2024-02-06","ym":"2024-02","product":"Headphones","category":"Electronics","quantity":5,"unit_price":100,"cost":60,"region":"Alexandria","revenue":500,"total_cost":300,"profit":200},{"order_id":1065,"date":"2024-01-10","ym":"2024-01","product":"Table","category":"Furniture","quantity":1,"unit_price":350,"cost":220,"region":"Suez","revenue":350,"total_cost":220,"profit":130},{"order_id":1066,"date":"2024-03-28","ym":"2024-03","product":"Table","category":"Furniture","quantity":4,"unit_price":350,"cost":220,"region":"Alexandria","revenue":1400,"total_cost":880,"profit":520},{"order_id":1067,"date":"2024-02-04","ym":"2024-02","product":"Table","category":"Furniture","quantity":2,"unit_price":350,"cost":220,"region":"Suez","revenue":700,"total_cost":440,"profit":260},{"order_id":1068,"date":"2024-03-15","ym":"2024-03","product":"Chair","category":"Furniture","quantity":3,"unit_price":150,"cost":90,"region":"Giza","revenue":450,"total_cost":270,"profit":180},{"order_id":1069,"date":"2024-01-24","ym":"2024-01","product":"Monitor","category":"Electronics","quantity":4,"unit_price":400,"cost":250,"region":"Suez","revenue":1600,"total_cost":1000,"profit":600},{"order_id":1070,"date":"2024-03-01","ym":"2024-03","product":"Chair","category":"Furniture","quantity":4,"unit_price":150,"cost":90,"region":"Alexandria","revenue":600,"total_cost":360,"profit":240},{"order_id":1071,"date":"2024-02-29","ym":"2024-02","product":"Phone","category":"Electronics","quantity":2,"unit_price":600,"cost":400,"region":"Tanta","revenue":1200,"total_cost":800,"profit":400},{"order_id":1072,"date":"2024-02-12","ym":"2024-02","product":"Desk","category":"Furniture","quantity":4,"unit_price":300,"cost":200,"region":"Alexandria","revenue":1200,"total_cost":800,"profit":400},{"order_id":1073,"date":"2024-02-10","ym":"2024-02","product":"Laptop","category":"Electronics","quantity":2,"unit_price":1200,"cost":900,"region":"Suez","revenue":2400,"total_cost":1800,"profit":600},{"order_id":1074,"date":"2024-01-12","ym":"2024-01","product":"Monitor","category":"Electronics","quantity":5,"unit_price":400,"cost":250,"region":"Tanta","revenue":2000,"total_cost":1250,"profit":750},{"order_id":1075,"date":"2024-02-18","ym":"2024-02","product":"Chair","category":"Furniture","quantity":2,"unit_price":150,"cost":90,"region":"Cairo","revenue":300,"total_cost":180,"profit":120},{"order_id":1076,"date":"2024-03-18","ym":"2024-03","product":"Chair","category":"Furniture","quantity":2,"unit_price":150,"cost":90,"region":"Giza","revenue":300,"total_cost":180,"profit":120},{"order_id":1077,"date":"2024-02-15","ym":"2024-02","product":"Chair","category":"Furniture","quantity":2,"unit_price":150,"cost":90,"region":"Tanta","revenue":300,"total_cost":180,"profit":120},{"order_id":1078,"date":"2024-03-11","ym":"2024-03","product":"Chair","category":"Furniture","quantity":3,"unit_price":150,"cost":90,"region":"Suez","revenue":450,"total_cost":270,"profit":180},{"order_id":1079,"date":"2024-03-18","ym":"2024-03","product":"Phone","category":"Electronics","quantity":2,"unit_price":600,"cost":400,"region":"Tanta","revenue":1200,"total_cost":800,"profit":400},{"order_id":1080,"date":"2024-01-31","ym":"2024-01","product":"Monitor","category":"Electronics","quantity":2,"unit_price":400,"cost":250,"region":"Alexandria","revenue":800,"total_cost":500,"profit":300},{"order_id":1081,"date":"2024-01-07","ym":"2024-01","product":"Desk","category":"Furniture","quantity":1,"unit_price":300,"cost":200,"region":"Suez","revenue":300,"total_cost":200,"profit":100},{"order_id":1082,"date":"2024-01-17","ym":"2024-01","product":"Phone","category":"Electronics","quantity":4,"unit_price":600,"cost":400,"region":"Tanta","revenue":2400,"total_cost":1600,"profit":800},{"order_id":1083,"date":"2024-02-17","ym":"2024-02","product":"Chair","category":"Furniture","quantity":2,"unit_price":150,"cost":90,"region":"Alexandria","revenue":300,"total_cost":180,"profit":120},{"order_id":1084,"date":"2024-02-20","ym":"2024-02","product":"Table","category":"Furniture","quantity":5,"unit_price":350,"cost":220,"region":"Alexandria","revenue":1750,"total_cost":1100,"profit":650},{"order_id":1085,"date":"2024-02-16","ym":"2024-02","product":"Phone","category":"Electronics","quantity":5,"unit_price":600,"cost":400,"region":"Cairo","revenue":3000,"total_cost":2000,"profit":1000},{"order_id":1086,"date":"2024-03-28","ym":"2024-03","product":"Phone","category":"Electronics","quantity":5,"unit_price":600,"cost":400,"region":"Suez","revenue":3000,"total_cost":2000,"profit":1000},{"order_id":1087,"date":"2024-01-25","ym":"2024-01","product":"Phone","category":"Electronics","quantity":4,"unit_price":600,"cost":400,"region":"Giza","revenue":2400,"total_cost":1600,"profit":800},{"order_id":1088,"date":"2024-01-30","ym":"2024-01","product":"Monitor","category":"Electronics","quantity":2,"unit_price":400,"cost":250,"region":"Mansoura","revenue":800,"total_cost":500,"profit":300},{"order_id":1089,"date":"2024-01-04","ym":"2024-01","product":"Chair","category":"Furniture","quantity":5,"unit_price":150,"cost":90,"region":"Alexandria","revenue":750,"total_cost":450,"profit":300},{"order_id":1090,"date":"2024-02-01","ym":"2024-02","product":"Monitor","category":"Electronics","quantity":2,"unit_price":400,"cost":250,"region":"Alexandria","revenue":800,"total_cost":500,"profit":300},{"order_id":1091,"date":"2024-03-18","ym":"2024-03","product":"Desk","category":"Furniture","quantity":4,"unit_price":300,"cost":200,"region":"Alexandria","revenue":1200,"total_cost":800,"profit":400},{"order_id":1092,"date":"2024-03-17","ym":"2024-03","product":"Table","category":"Furniture","quantity":3,"unit_price":350,"cost":220,"region":"Mansoura","revenue":1050,"total_cost":660,"profit":390},{"order_id":1093,"date":"2024-03-10","ym":"2024-03","product":"Headphones","category":"Electronics","quantity":3,"unit_price":100,"cost":60,"region":"Giza","revenue":300,"total_cost":180,"profit":120},{"order_id":1094,"date":"2024-02-16","ym":"2024-02","product":"Monitor","category":"Electronics","quantity":4,"unit_price":400,"cost":250,"region":"Tanta","revenue":1600,"total_cost":1000,"profit":600},{"order_id":1095,"date":"2024-01-12","ym":"2024-01","product":"Phone","category":"Electronics","quantity":5,"unit_price":600,"cost":400,"region":"Suez","revenue":3000,"total_cost":2000,"profit":1000},{"order_id":1096,"date":"2024-02-03","ym":"2024-02","product":"Laptop","category":"Electronics","quantity":1,"unit_price":1200,"cost":900,"region":"Tanta","revenue":1200,"total_cost":900,"profit":300},{"order_id":1097,"date":"2024-02-04","ym":"2024-02","product":"Desk","category":"Furniture","quantity":4,"unit_price":300,"cost":200,"region":"Alexandria","revenue":1200,"total_cost":800,"profit":400},{"order_id":1098,"date":"2024-02-27","ym":"2024-02","product":"Monitor","category":"Electronics","quantity":1,"unit_price":400,"cost":250,"region":"Giza","revenue":400,"total_cost":250,"profit":150},{"order_id":1099,"date":"2024-02-06","ym":"2024-02","product":"Chair","category":"Furniture","quantity":1,"unit_price":150,"cost":90,"region":"Mansoura","revenue":150,"total_cost":90,"profit":60},{"order_id":1100,"date":"2024-03-19","ym":"2024-03","product":"Phone","category":"Electronics","quantity":3,"unit_price":600,"cost":400,"region":"Cairo","revenue":1800,"total_cost":1200,"profit":600}];
const PALETTE=['#3b82f6','#06b6d4','#8b5cf6','#10b981','#f59e0b','#ef4444','#ec4899'];
const MONTH_LABELS={'2024-01':'Jan 2024','2024-02':'Feb 2024','2024-03':'Mar 2024'};
let charts={};
function fmt(n){return '$'+n.toLocaleString();}
function getFiltered(){
  const from=document.getElementById('dateFrom').value,to=document.getElementById('dateTo').value,
        cat=document.getElementById('catFilter').value,region=document.getElementById('regionFilter').value,
        product=document.getElementById('productFilter').value;
  return RAW.filter(r=>{
    if(from&&r.date<from)return false;if(to&&r.date>to)return false;
    if(cat!=='all'&&r.category!==cat)return false;if(region!=='all'&&r.region!==region)return false;
    if(product!=='all'&&r.product!==product)return false;return true;});
}
function aggregate(data,key,val){const m={};data.forEach(r=>{m[r[key]]=(m[r[key]]||0)+r[val];});return m;}
function sortedEntries(obj,desc=true){return Object.entries(obj).sort((a,b)=>desc?b[1]-a[1]:a[1]-b[1]);}
function updateKPIs(data){
  const rev=data.reduce((s,r)=>s+r.revenue,0),prof=data.reduce((s,r)=>s+r.profit,0),
        margin=rev?((prof/rev)*100).toFixed(1):0;
  document.getElementById('kpiRevenue').textContent=fmt(rev);
  document.getElementById('kpiProfit').textContent=fmt(prof);
  document.getElementById('kpiOrders').textContent=data.length;
  document.getElementById('kpiRevSub').textContent=`Avg order: ${fmt(Math.round(rev/(data.length||1)))}`;
  document.getElementById('kpiProfSub').textContent=`Margin: ${margin}%`;
  document.getElementById('kpiOrdSub').textContent=`${data.length} of 100 records shown`;
}
function updateInsights(data){
  if(!data.length)return;
  const byProd=aggregate(data,'product','revenue'),byReg=aggregate(data,'region','revenue'),
        byMonth=aggregate(data,'ym','revenue'),totalRev=data.reduce((s,r)=>s+r.revenue,0),
        totalProf=data.reduce((s,r)=>s+r.profit,0);
  const topProd=sortedEntries(byProd)[0],topReg=sortedEntries(byReg)[0],topMonth=sortedEntries(byMonth)[0];
  const margin=totalRev?((totalProf/totalRev)*100).toFixed(1):0;
  document.getElementById('insTopProd').textContent=topProd?topProd[0]:'—';
  document.getElementById('insTopProdSub').textContent=topProd?fmt(topProd[1])+' revenue':'—';
  document.getElementById('insBestRegion').textContent=topReg?topReg[0]:'—';
  document.getElementById('insBestRegionSub').textContent=topReg?fmt(topReg[1])+' revenue':'—';
  document.getElementById('insBestMonth').textContent=topMonth?(MONTH_LABELS[topMonth[0]]||topMonth[0]):'—';
  document.getElementById('insBestMonthSub').textContent=topMonth?fmt(topMonth[1])+' revenue':'—';
  document.getElementById('insMargin').textContent=margin+'%';
  document.getElementById('insMarginSub').textContent=parseFloat(margin)>30?'✅ Healthy':'⚠️ Watch closely';
}
function updateTable(data){
  const sorted=[...data].sort((a,b)=>b.revenue-a.revenue).slice(0,10);
  document.getElementById('topOrdersBody').innerHTML=sorted.map(r=>`<tr><td style="color:var(--muted);font-size:12px">#${r.order_id}</td><td>${r.date}</td><td><strong>${r.product}</strong></td><td><span class="cat-badge cat-${r.category.toLowerCase()}">${r.category}</span></td><td>${r.region}</td><td>${r.quantity}</td><td style="color:#60a5fa;font-weight:600">${fmt(r.revenue)}</td><td style="color:#34d399">${fmt(r.profit)}</td></tr>`).join('');
}
function destroyChart(id){if(charts[id]){charts[id].destroy();delete charts[id];}}
function chartOpts(label){return{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'#1a2235',titleColor:'#f1f5f9',bodyColor:'#94a3b8',callbacks:{label:c=>` ${label}: ${fmt(c.raw)}`}}},scales:{x:{ticks:{color:'#64748b',font:{family:'DM Sans',size:11}},grid:{color:'rgba(30,45,69,0.5)'}},y:{ticks:{color:'#64748b',font:{family:'DM Sans',size:11},callback:v=>'$'+v.toLocaleString()},grid:{color:'rgba(30,45,69,0.5)'}}}};}
function updateCharts(data){
  const months=['2024-01','2024-02','2024-03'],byMonth=aggregate(data,'ym','revenue');
  destroyChart('line');
  charts['line']=new Chart(document.getElementById('lineChart'),{type:'line',data:{labels:months.map(m=>MONTH_LABELS[m]),datasets:[{label:'Revenue',data:months.map(m=>byMonth[m]||0),borderColor:'#3b82f6',backgroundColor:'rgba(59,130,246,0.1)',borderWidth:2.5,tension:0.4,fill:true,pointBackgroundColor:'#3b82f6',pointRadius:5,pointHoverRadius:7}]},options:chartOpts('Revenue ($)')});
  const byProd=aggregate(data,'product','revenue'),prodEntries=sortedEntries(byProd);
  destroyChart('productBar');
  charts['productBar']=new Chart(document.getElementById('productBar'),{type:'bar',data:{labels:prodEntries.map(e=>e[0]),datasets:[{label:'Revenue',data:prodEntries.map(e=>e[1]),backgroundColor:PALETTE,borderRadius:6,borderSkipped:false}]},options:chartOpts('Revenue ($)')});
  const byCat=aggregate(data,'category','revenue');
  destroyChart('pie');
  charts['pie']=new Chart(document.getElementById('pieChart'),{type:'doughnut',data:{labels:Object.keys(byCat),datasets:[{data:Object.values(byCat),backgroundColor:['#3b82f6','#f59e0b'],borderColor:'#111827',borderWidth:3,hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{color:'#94a3b8',font:{family:'DM Sans',size:12},padding:16}},tooltip:{callbacks:{label:c=>` ${c.label}: ${fmt(c.raw)} (${((c.raw/Object.values(byCat).reduce((a,b)=>a+b,0))*100).toFixed(1)}%)`},backgroundColor:'#1a2235',titleColor:'#f1f5f9',bodyColor:'#94a3b8'}}}});
  const byReg=aggregate(data,'region','revenue'),regEntries=sortedEntries(byReg);
  destroyChart('regionBar');
  charts['regionBar']=new Chart(document.getElementById('regionBar'),{type:'bar',data:{labels:regEntries.map(e=>e[0]),datasets:[{label:'Revenue',data:regEntries.map(e=>e[1]),backgroundColor:regEntries.map((_,i)=>PALETTE[i%PALETTE.length]),borderRadius:6,borderSkipped:false}]},options:chartOpts('Revenue ($)')});
  const byProdProfit=aggregate(data,'product','profit'),profEntries=sortedEntries(byProdProfit);
  destroyChart('profitBar');
  charts['profitBar']=new Chart(document.getElementById('profitBar'),{type:'bar',data:{labels:profEntries.map(e=>e[0]),datasets:[{label:'Profit',data:profEntries.map(e=>e[1]),backgroundColor:'#10b981',borderRadius:6,borderSkipped:false}]},options:chartOpts('Profit ($)')});
}
function update(){const data=getFiltered();updateKPIs(data);updateInsights(data);updateCharts(data);updateTable(data);}
function resetFilters(){document.getElementById('dateFrom').value='2024-01-01';document.getElementById('dateTo').value='2024-03-31';document.getElementById('catFilter').value='all';document.getElementById('regionFilter').value='all';document.getElementById('productFilter').value='all';update();}
['dateFrom','dateTo','catFilter','regionFilter','productFilter'].forEach(id=>{document.getElementById(id).addEventListener('change',update);});
Chart.defaults.color='#64748b';Chart.defaults.font.family='DM Sans';
update();
</script>
</body>
</html>
"""

import os, webbrowser, tempfile

def main():
    # Save HTML file next to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path  = os.path.join(script_dir, "sales_dashboard.html")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML)

    print("=" * 55)
    print("  📊 Sales Performance Dashboard")
    print("=" * 55)
    print(f"  ✅ File saved: {html_path}")
    print("  🌐 Opening in your browser...")
    print("=" * 55)

    webbrowser.open(f"file://{html_path}")

if __name__ == "__main__":
    main()
