# build_dashboard.py
import json

print("Reading data_clean.json...")
with open("data_clean.json", "r", encoding="utf-8") as f:
    data_json = f.read()

# Build index.html
html_content = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rainfall Intelligence & Predictive Analytics Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root {
  /* Functional Palette: Targeted & Minimalist */
  --color-surplus: #10B981;      /* Emerald Green (Normal / High Rainfall) */
  --color-warning: #F59E0B;      /* Warm Amber (Moderate / Deficit Risk) */
  --color-danger:  #EF4444;      /* Crimson Red (Severe / Drought Anomaly) */
  --color-primary: #1D4ED8;      /* Deep Cobalt Blue (Primary Metric Focus) */
  --color-primary-light: #2563EB;
  --color-primary-subtle: rgba(29, 78, 216, 0.08);

  /* Light Theme (Default Monochromatic Slate) */
  --bg-app: #f8fafc;
  --bg-surface: #ffffff;
  --bg-surface-elevated: #ffffff;
  --bg-surface-muted: #f1f5f9;
  --bg-hover: #e2e8f0;
  --border-subtle: #e2e8f0;
  --border-hover: #cbd5e1;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --text-faint: #94a3b8;
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 4px 14px -2px rgba(15, 23, 42, 0.07);
  --shadow-lg: 0 12px 28px -4px rgba(15, 23, 42, 0.09);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --nav-width: 260px;
}

body.theme-night {
  /* Sleek Night Slate Monochromatic */
  --bg-app: #0f172a;
  --bg-surface: #1e293b;
  --bg-surface-elevated: #243248;
  --bg-surface-muted: #172233;
  --bg-hover: #334155;
  --border-subtle: #334155;
  --border-hover: #475569;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-faint: #64748b;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 14px -2px rgba(0, 0, 0, 0.35);
  --shadow-lg: 0 12px 28px -4px rgba(0, 0, 0, 0.45);
  --color-primary-subtle: rgba(37, 99, 235, 0.15);
}

body.theme-dark {
  /* Clean Minimalist Dark Monochromatic */
  --bg-app: #030712;
  --bg-surface: #0b1120;
  --bg-surface-elevated: #111827;
  --bg-surface-muted: #070d19;
  --bg-hover: #1f2937;
  --border-subtle: #1f2937;
  --border-hover: #374151;
  --text-main: #f9fafb;
  --text-muted: #9ca3af;
  --text-faint: #4b5563;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 14px -2px rgba(0, 0, 0, 0.6);
  --shadow-lg: 0 12px 28px -4px rgba(0, 0, 0, 0.7);
  --color-primary-subtle: rgba(29, 78, 216, 0.2);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: var(--bg-app);
  color: var(--text-main);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
  transition: background-color 0.12s ease, color 0.12s ease;
}

button, input, select {
  font: inherit;
  color: inherit;
}

/* Zero-click hover transition speed: strictly under 100ms */
.hover-snap {
  transition: all 0.08s cubic-bezier(0.16, 1, 0.3, 1);
}

/* App Layout */
.app-container {
  display: flex;
  min-height: 100vh;
}

/* Sidebar Navigation */
.sidebar {
  width: var(--nav-width);
  background: var(--bg-surface);
  border-right: 1px solid var(--border-subtle);
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 50;
  display: flex;
  flex-direction: column;
  padding: 20px 14px;
}

.brand-section {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 10px 22px;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 18px;
}

.brand-icon {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-md);
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  display: grid;
  place-items: center;
  font-size: 20px;
  border: 1px solid rgba(29, 78, 216, 0.2);
}

.brand-info h2 {
  font-size: 14px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-main);
}

.brand-info p {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 500;
}

/* Zero-Click Hover Nav Tabs */
.nav-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-faint);
  padding: 6px 12px 2px;
}

.nav-btn {
  border: 1px solid transparent;
  background: transparent;
  text-align: left;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  font-size: 13px;
  position: relative;
  cursor: pointer;
  transition: all 0.07s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Strict Zero-Click Requirement: Instant active styling on hover */
.nav-btn:hover {
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  border-color: rgba(29, 78, 216, 0.2);
  transform: translateX(3px);
}

.nav-btn.active {
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  border-color: rgba(29, 78, 216, 0.25);
  font-weight: 700;
}

.nav-btn.active::before {
  content: "";
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 3px;
  border-radius: 4px;
  background: var(--color-primary-light);
}

.nav-btn .nav-ico {
  width: 18px;
  font-size: 15px;
  text-align: center;
}

.nav-badge {
  margin-left: auto;
  font-size: 10px;
  padding: 2px 7px;
  border-radius: 20px;
  background: var(--bg-surface-muted);
  color: var(--text-muted);
  font-weight: 700;
}

.sidebar-footer {
  margin-top: auto;
  border-top: 1px solid var(--border-subtle);
  padding: 14px 10px 4px;
}

.telemetry-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: var(--bg-surface-muted);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  font-size: 11px;
  color: var(--text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-surplus);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
  animation: pulseDot 2s infinite ease-in-out;
}

@keyframes pulseDot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.85); }
}

/* Main Content Area */
.main-wrapper {
  margin-left: var(--nav-width);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Topbar */
.topbar {
  height: 66px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 40;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title-badge {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 4px 9px;
  border-radius: var(--radius-sm);
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  border: 1px solid rgba(29, 78, 216, 0.2);
}

.live-indicator {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* Zero-Click Theme Mode Dropdown / Hover Chips */
.theme-switcher-container {
  display: flex;
  align-items: center;
  background: var(--bg-surface-muted);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 3px;
  gap: 3px;
}

.theme-pill-btn {
  border: 0;
  background: transparent;
  font-size: 11px;
  font-weight: 600;
  padding: 5px 9px;
  border-radius: 6px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.07s ease;
}

/* Hover activates theme immediately */
.theme-pill-btn:hover {
  background: var(--bg-surface);
  color: var(--text-main);
  box-shadow: var(--shadow-sm);
}

.theme-pill-btn.active {
  background: var(--bg-surface);
  color: var(--color-primary-light);
  font-weight: 700;
  box-shadow: var(--shadow-sm);
}

.dataset-meta-pill {
  font-size: 11px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface-muted);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
}

/* Content Container */
.content-area {
  padding: 28px 32px 48px;
  max-width: 1540px;
  margin: 0 auto;
  width: 100%;
}

/* Page Section Visibility */
.page-section {
  display: none;
  animation: fadeIn 0.1s ease-out;
}

.page-section.active {
  display: block;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Page Headings */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 22px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-main);
}

.page-header p {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 3px;
}

/* Hover HUD Card */
.hover-hud {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-sm);
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
}

.hover-hud strong {
  color: var(--color-primary-light);
}

/* Grids & Cards */
.grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 16px;
  margin-bottom: 16px;
}

.grid-2-equal {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: border-color 0.08s ease, transform 0.08s ease, box-shadow 0.08s ease;
  position: relative;
  overflow: hidden;
}

.card:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow-md);
}

/* KPI Card */
.kpi-card {
  padding: 20px;
}

.kpi-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kpi-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.kpi-value {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-top: 8px;
  color: var(--text-main);
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.kpi-unit {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
}

.kpi-footer {
  margin-top: 8px;
  font-size: 11.5px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Functional Accents for Pills */
.pill-accent {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
}

.pill-surplus {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.25);
}

body.theme-night .pill-surplus, body.theme-dark .pill-surplus {
  background: rgba(16, 185, 129, 0.18);
  color: #34d399;
}

.pill-warning {
  background: rgba(245, 158, 11, 0.12);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.25);
}

body.theme-night .pill-warning, body.theme-dark .pill-warning {
  background: rgba(245, 158, 11, 0.18);
  color: #fbbf24;
}

.pill-danger {
  background: rgba(239, 68, 68, 0.12);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.25);
}

body.theme-night .pill-danger, body.theme-dark .pill-danger {
  background: rgba(239, 68, 68, 0.18);
  color: #f87171;
}

.pill-primary {
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  border: 1px solid rgba(29, 78, 216, 0.25);
}

/* Panel Design */
.panel {
  padding: 20px 22px;
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.panel-title {
  font-size: 14px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: var(--text-main);
}

.panel-subtitle {
  font-size: 11.5px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* Chart Container */
.chart-box {
  position: relative;
  width: 100%;
  height: 310px;
}

.chart-box.compact {
  height: 250px;
}

.chart-box.large {
  height: 360px;
}

/* Hover-Activated Custom Select / Dropdown Component (Strict Zero-Click) */
.hover-select-group {
  position: relative;
  display: inline-block;
}

.hover-select-trigger {
  padding: 8px 14px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 700;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.08s ease;
}

.hover-select-trigger:hover, .hover-select-group:hover .hover-select-trigger {
  border-color: var(--color-primary-light);
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.1);
  color: var(--color-primary-light);
}

.hover-dropdown-panel {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 240px;
  max-height: 280px;
  overflow-y: auto;
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-hover);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-lg);
  padding: 6px;
  z-index: 100;
  display: none;
  margin-top: 4px;
}

/* Zero-Click Open on Mouseenter / Hover */
.hover-select-group:hover .hover-dropdown-panel {
  display: block;
}

.hover-dropdown-item {
  padding: 7px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-main);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.05s ease;
}

/* Zero-click hover selection: hovering immediately selects */
.hover-dropdown-item:hover {
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  font-weight: 700;
}

.hover-dropdown-item.selected {
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  font-weight: 800;
}

/* Quick Interactive Chip Selectors (Hover Activated) */
.chip-bar {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding-bottom: 6px;
  margin-bottom: 14px;
}

.hover-chip {
  padding: 6px 12px;
  background: var(--bg-surface-muted);
  border: 1px solid var(--border-subtle);
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.07s ease;
}

.hover-chip:hover {
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  border-color: rgba(29, 78, 216, 0.3);
  transform: translateY(-1px);
}

.hover-chip.active {
  background: var(--color-primary-light);
  color: #ffffff;
  border-color: var(--color-primary-light);
  font-weight: 700;
}

/* Rank Lists & Leaderboards */
.rank-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 310px;
  overflow-y: auto;
  padding-right: 4px;
}

.rank-row {
  display: grid;
  grid-template-columns: 28px 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 7px 10px;
  border-radius: var(--radius-sm);
  background: var(--bg-surface-muted);
  border: 1px solid transparent;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.07s cubic-bezier(0.16, 1, 0.3, 1);
}

.rank-row:hover {
  background: var(--color-primary-subtle);
  border-color: rgba(29, 78, 216, 0.2);
  transform: translateX(3px);
}

.rank-num {
  font-weight: 800;
  color: var(--text-faint);
  font-size: 11px;
  text-align: center;
}

.rank-name {
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rank-bar-bg {
  height: 5px;
  background: var(--border-subtle);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 4px;
}

.rank-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: var(--color-primary-light);
  transition: width 0.3s ease;
}

.rank-val {
  font-weight: 800;
  font-size: 12px;
  color: var(--text-main);
  text-align: right;
}

/* Prediction / Forecast Layout */
.prediction-grid {
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 16px;
}

.prediction-hero-card {
  padding: 24px;
  border-radius: var(--radius-md);
  background: linear-gradient(145deg, var(--bg-surface), var(--bg-surface-elevated));
  border: 1px solid var(--border-subtle);
}

.forecast-figure-box {
  margin: 14px 0 10px;
}

.forecast-figure {
  font-size: 42px;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--color-primary-light);
  line-height: 1;
}

.forecast-delta {
  font-size: 12px;
  font-weight: 700;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.stat-pills-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin: 16px 0;
}

.stat-box {
  background: var(--bg-surface-muted);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px;
  text-align: left;
}

.stat-box-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}

.stat-box-val {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-main);
  margin-top: 2px;
}

/* Data Table & Explorer */
.table-wrapper {
  overflow-x: auto;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  text-align: left;
}

.data-table th {
  background: var(--bg-surface-muted);
  padding: 10px 14px;
  font-weight: 700;
  font-size: 10.5px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border-subtle);
  white-space: nowrap;
}

.data-table td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-main);
  white-space: nowrap;
}

/* Zero-Click Table Row Hover: highlights row and updates live flyout */
.data-table tr {
  cursor: pointer;
  transition: background-color 0.05s ease;
}

.data-table tbody tr:hover td {
  background: var(--color-primary-subtle);
}

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}

.search-input-box {
  position: relative;
  width: 320px;
}

.search-input {
  width: 100%;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 8px 12px 8px 34px;
  font-size: 12px;
  outline: none;
  transition: border-color 0.08s ease, box-shadow 0.08s ease;
}

.search-input:focus {
  border-color: var(--color-primary-light);
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.1);
}

.search-icon-inside {
  position: absolute;
  left: 11px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 13px;
  color: var(--text-faint);
}

/* Live Row Telemetry Flyout Card */
.row-inspector-card {
  padding: 14px 18px;
  background: var(--bg-surface-muted);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  margin-top: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  font-size: 12px;
}

.sparkline-container {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 28px;
}

.spark-bar {
  width: 6px;
  background: var(--color-primary-light);
  border-radius: 2px 2px 0 0;
  transition: height 0.15s ease;
}

/* Pagination Bar */
.pagination-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0 0;
  font-size: 12px;
  color: var(--text-muted);
}

.page-chip-list {
  display: flex;
  gap: 4px;
}

.page-chip {
  padding: 4px 9px;
  border-radius: 6px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.06s ease;
}

.page-chip:hover {
  background: var(--color-primary-subtle);
  color: var(--color-primary-light);
  border-color: rgba(29, 78, 216, 0.2);
}

.page-chip.active {
  background: var(--color-primary-light);
  color: #ffffff;
  border-color: var(--color-primary-light);
}

/* Insights Strip */
.insight-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 16px;
}

.insight-item {
  padding: 16px;
  background: var(--bg-surface-muted);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  font-size: 12px;
  transition: all 0.08s ease;
}

.insight-item:hover {
  border-color: var(--border-hover);
  transform: translateY(-1px);
}

.insight-item strong {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 4px;
}

.insight-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary-light);
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
  .grid-2 { grid-template-columns: 1fr; }
  .prediction-grid { grid-template-columns: 1fr; }
  .insight-strip { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .sidebar { width: 70px; padding: 14px 6px; }
  .brand-info, .nav-label, .nav-btn span:not(.nav-ico), .nav-badge, .sidebar-footer { display: none; }
  .nav-btn { justify-content: center; padding: 12px 0; }
  .main-wrapper { margin-left: 70px; }
  .topbar { padding: 0 16px; }
  .content-area { padding: 18px 16px; }
  .grid-4, .grid-2-equal, .grid-3, .insight-strip { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; align-items: flex-start; gap: 8px; }
}
</style>
</head>
<body>

<div class="app-container">
  <!-- SIDEBAR NAVIGATION (Zero-Click Hover Activated) -->
  <aside class="sidebar">
    <div class="brand-section">
      <div class="brand-icon">🌧</div>
      <div class="brand-info">
        <h2>Rainfall Intelligence</h2>
        <p>National Meteorological Portal</p>
      </div>
    </div>

    <div class="nav-label">Navigation (Zero-Click)</div>
    <nav class="nav-group" id="mainNav">
      <button class="nav-btn active hover-snap" data-target="overview" id="nav-overview">
        <span class="nav-ico">⌂</span>
        <span>Overview</span>
        <span class="nav-badge">115y</span>
      </button>
      <button class="nav-btn hover-snap" data-target="analytics" id="nav-analytics">
        <span class="nav-ico">▥</span>
        <span>Rainfall Analytics</span>
      </button>
      <button class="nav-btn hover-snap" data-target="forecast" id="nav-forecast">
        <span class="nav-ico">◈</span>
        <span>OLS Prediction</span>
        <span class="nav-badge pill-surplus" style="font-size:9px">AI/OLS</span>
      </button>
      <button class="nav-btn hover-snap" data-target="risk" id="nav-risk">
        <span class="nav-ico">△</span>
        <span>Anomaly & Risk</span>
      </button>
      <button class="nav-btn hover-snap" data-target="explorer" id="nav-explorer">
        <span class="nav-ico">▤</span>
        <span>Data Explorer</span>
        <span class="nav-badge">4.7k</span>
      </button>
    </nav>

    <div class="sidebar-footer">
      <div class="telemetry-chip">
        <div class="status-dot"></div>
        <div>
          <b style="color:var(--text-main)">Hover Navigation</b>
          <div style="font-size:10px;color:var(--text-muted)">Instant Zero-Click Mode</div>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN WRAPPER -->
  <main class="main-wrapper">
    <!-- TOPBAR -->
    <header class="topbar">
      <div class="topbar-left">
        <span class="page-title-badge" id="activeSectionBadge">OVERVIEW</span>
        <div class="live-indicator">
          <span>India Historic & Predictive Rain Intelligence (1901–2015)</span>
        </div>
      </div>
      <div class="topbar-right">
        <!-- Zero-Click Theme Mode Buttons -->
        <div class="theme-switcher-container">
          <button class="theme-pill-btn active" data-theme="light" title="Light Mode">☼ Light</button>
          <button class="theme-pill-btn" data-theme="night" title="Night Slate Mode">◐ Night</button>
          <button class="theme-pill-btn" data-theme="dark" title="Dark Mode">☾ Dark</button>
        </div>
        <div class="dataset-meta-pill">36 Subdivisions · 641 Districts</div>
      </div>
    </header>

    <!-- CONTENT AREA -->
    <div class="content-area">

      <!-- ================= SECTION 1: OVERVIEW ================= -->
      <section class="page-section active" id="overview">
        <div class="page-header">
          <div>
            <h1>National Rainfall Intelligence</h1>
            <p>Aggregated national meteorological profile, long-term trends, and extreme variations.</p>
          </div>
          <div class="hover-hud" id="overviewHud">
            <span>Historical Period: <strong>1901–2015</strong></span>
            <span>·</span>
            <span>Subdivisions: <strong>36</strong></span>
          </div>
        </div>

        <!-- KPI Grid -->
        <div class="grid-4">
          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">National Annual Average</span>
              <span class="pill-accent pill-primary">Overall</span>
            </div>
            <div class="kpi-value"><span id="kpiAvgValue">—</span><span class="kpi-unit">mm</span></div>
            <div class="kpi-footer">Across 115 continuous observation years</div>
          </div>

          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">Wettest Subdivision</span>
              <span class="pill-accent pill-surplus" id="kpiWetPeakPill">Wettest</span>
            </div>
            <div class="kpi-value" style="font-size:20px; line-height:1.2; margin-top:12px" id="kpiWetName">—</div>
            <div class="kpi-footer"><span id="kpiWetAnnual" style="font-weight:700; color:var(--color-surplus)">— mm</span> avg annual</div>
          </div>

          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">Driest Subdivision</span>
              <span class="pill-accent pill-danger" id="kpiDryPeakPill">Critical</span>
            </div>
            <div class="kpi-value" style="font-size:20px; line-height:1.2; margin-top:12px" id="kpiDryName">—</div>
            <div class="kpi-footer"><span id="kpiDryAnnual" style="font-weight:700; color:var(--color-danger)">— mm</span> avg annual</div>
          </div>

          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">SW Monsoon Share</span>
              <span class="pill-accent pill-warning">Jun–Sep</span>
            </div>
            <div class="kpi-value"><span id="kpiMonsoonShare">—</span><span class="kpi-unit">%</span></div>
            <div class="kpi-footer">Dominant component of annual volume</div>
          </div>
        </div>

        <!-- Trend & Leaderboard Grid -->
        <div class="grid-2">
          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">115-Year National Rainfall Trend (1901–2015)</div>
                <div class="panel-subtitle">National annual mean rainfall series with OLS linear trendline</div>
              </div>
              <div class="hover-hud" id="trendHoverHud">Hover line to inspect year</div>
            </div>
            <div class="chart-box"><canvas id="trendChart"></canvas></div>
          </div>

          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">Subdivision Rankings (Top 10)</div>
                <div class="panel-subtitle">Hover row to inspect regional distribution</div>
              </div>
              <span class="pill-accent pill-primary" id="rankSubCount">Top 10 of 36</span>
            </div>
            <div class="rank-list" id="overviewRankList"></div>
          </div>
        </div>

        <!-- Monthly & Seasonal Grid -->
        <div class="grid-2-equal">
          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">Average Monthly Distribution (Jan–Dec)</div>
                <div class="panel-subtitle">Concentration peaks sharply during monsoon months (Jul–Aug)</div>
              </div>
              <span class="pill-accent pill-surplus" id="monthlyPeakHud">Peak: July</span>
            </div>
            <div class="chart-box compact"><canvas id="monthlyChart"></canvas></div>
          </div>

          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">Seasonal Distribution Breakdown</div>
                <div class="panel-subtitle">Four official meteorological periods across India</div>
              </div>
              <span class="pill-accent pill-warning">SW Monsoon (74%)</span>
            </div>
            <div class="chart-box compact"><canvas id="seasonalChart"></canvas></div>
          </div>
        </div>

        <!-- Insights Strip -->
        <div class="card panel">
          <div class="panel-title">Climatological Findings & Intelligence Notes</div>
          <div class="insight-strip" id="overviewInsights"></div>
        </div>
      </section>

      <!-- ================= SECTION 2: ANALYTICS ================= -->
      <section class="page-section" id="analytics">
        <div class="page-header">
          <div>
            <h1>Subdivision & District Analytics</h1>
            <p>High-resolution inspection of monthly curves, seasonal distributions, and district normal leaderboards.</p>
          </div>
          <div class="hover-hud" id="analyticsHud">Instant Zero-Click Parameter Switching</div>
        </div>

        <!-- Interactive Filter Bar (Hover Dropdown + Quick Chips) -->
        <div class="card panel" style="margin-bottom:16px">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:14px">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap">
              <!-- Custom Zero-Click Hover Subdivision Selector -->
              <div class="hover-select-group">
                <div class="hover-select-trigger" id="analyticsSubTrigger">
                  <span>Subdivision:</span>
                  <strong id="analyticsSubLabel">ANDAMAN & NICOBAR ISLANDS</strong>
                  <span>▾</span>
                </div>
                <div class="hover-dropdown-panel" id="analyticsSubDropdown"></div>
              </div>

              <!-- Year Filter (Hover Selector) -->
              <div class="hover-select-group">
                <div class="hover-select-trigger" id="analyticsYearTrigger">
                  <span>Year:</span>
                  <strong id="analyticsYearLabel">115-Year Historical Average</strong>
                  <span>▾</span>
                </div>
                <div class="hover-dropdown-panel" id="analyticsYearDropdown"></div>
              </div>

              <button class="hover-chip" id="analyticsResetBtn" style="border-radius:var(--radius-sm)">↺ Reset to Default</button>
            </div>

            <!-- Telemetry summary pill -->
            <div class="pill-accent pill-primary" id="analyticsSubStatPill">Annual Mean: — mm</div>
          </div>

          <!-- Quick Subdivision Chips for Fastest Zero-Click Navigation -->
          <div class="chip-bar" id="analyticsSubChips"></div>

          <!-- Charts Grid -->
          <div class="grid-2-equal" style="margin-top:10px; margin-bottom:0">
            <div>
              <div class="panel-title" style="font-size:13px">Monthly Precipitation Pattern</div>
              <div class="panel-subtitle">Jan through Dec volume for selected region</div>
              <div class="chart-box compact" style="margin-top:8px"><canvas id="analyticsMonthlyChart"></canvas></div>
            </div>
            <div>
              <div class="panel-title" style="font-size:13px">Seasonal Composition</div>
              <div class="panel-subtitle">Winter, Pre-Monsoon, Monsoon, Post-Monsoon</div>
              <div class="chart-box compact" style="margin-top:8px"><canvas id="analyticsSeasonalChart"></canvas></div>
            </div>
          </div>
        </div>

        <!-- District Extremes Leaderboards (641 Districts) -->
        <div class="grid-2-equal">
          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">Wettest Districts in India (Annual Normal)</div>
                <div class="panel-subtitle">Hover district to inspect rainfall metrics</div>
              </div>
              <span class="pill-accent pill-surplus">High Precipitation</span>
            </div>
            <div class="rank-list" id="wetDistrictsList"></div>
          </div>

          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">Driest Districts in India (Annual Normal)</div>
                <div class="panel-subtitle">High drought vulnerability / arid classifications</div>
              </div>
              <span class="pill-accent pill-danger">Extreme Aridity</span>
            </div>
            <div class="rank-list" id="dryDistrictsList"></div>
          </div>
        </div>
      </section>

      <!-- ================= SECTION 3: PREDICTION (OLS REGRESSION) ================= -->
      <section class="page-section" id="forecast">
        <div class="page-header">
          <div>
            <h1>Ordinary Least Squares (OLS) Rainfall Prediction</h1>
            <p>Rigorous linear trend estimation, slope coefficient metrics, and baseline projections dynamically re-rendered on parameter hover.</p>
          </div>
          <div class="pill-accent pill-surplus" id="olsModelTag">OLS Linear Trend Extrapolation Active</div>
        </div>

        <div class="prediction-grid">
          <!-- Control Panel & Parameters -->
          <div class="card panel">
            <div class="panel-title">Prediction Parameters</div>
            <div class="panel-subtitle">Hover over any subdivision or target year to project instantly without clicking.</div>

            <div style="margin-top:16px">
              <label style="font-size:11px; font-weight:700; text-transform:uppercase; color:var(--text-muted)">Select Subdivision (Hover to Switch)</label>
              <div class="hover-select-group" style="width:100%; margin-top:6px">
                <div class="hover-select-trigger" id="forecastSubTrigger" style="width:100%; justify-content:space-between">
                  <span id="forecastSubLabel">ANDAMAN & NICOBAR ISLANDS</span>
                  <span>▾</span>
                </div>
                <div class="hover-dropdown-panel" id="forecastSubDropdown" style="width:100%"></div>
              </div>
            </div>

            <!-- Target Year Selection (Hover Chips & Quick Scrub) -->
            <div style="margin-top:18px">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px">
                <label style="font-size:11px; font-weight:700; text-transform:uppercase; color:var(--text-muted)">Forecast Target Year</label>
                <span class="pill-accent pill-primary" id="forecastYearBadge">2026</span>
              </div>
              <div class="chip-bar" id="forecastYearChips">
                <span class="hover-chip active" data-year="2026">2026</span>
                <span class="hover-chip" data-year="2027">2027</span>
                <span class="hover-chip" data-year="2028">2028</span>
                <span class="hover-chip" data-year="2030">2030</span>
                <span class="hover-chip" data-year="2035">2035</span>
              </div>
              <input type="range" id="forecastYearSlider" min="2016" max="2035" value="2026" style="width:100%; accent-color:var(--color-primary-light); cursor:pointer">
            </div>

            <!-- Historical Baseline Window (Zero-Click Hover Parameter Testing) -->
            <div style="margin-top:18px">
              <label style="font-size:11px; font-weight:700; text-transform:uppercase; color:var(--text-muted)">Regression Baseline Window</label>
              <div class="chip-bar" id="baselineWindowChips" style="margin-top:6px">
                <span class="hover-chip active" data-window="all">Full (1901–2015)</span>
                <span class="hover-chip" data-window="1950">Post-1950</span>
                <span class="hover-chip" data-window="1980">Modern (1980+)</span>
              </div>
            </div>

            <!-- Scientific Methodology Disclaimer -->
            <div style="margin-top:18px; padding:12px; background:var(--bg-surface-muted); border-radius:var(--radius-sm); border:1px solid var(--border-subtle); font-size:11px; color:var(--text-muted); line-height:1.45">
              <b style="color:var(--text-main); display:block; margin-bottom:4px">OLS Model Specification</b>
              Fits \( y = \beta_0 + \beta_1 x \) where \( \beta_1 = \frac{\sum (x - \bar{x})(y - \bar{y})}{\sum (x - \bar{x})^2} \). Intended for empirical linear baseline analytics.
            </div>
          </div>

          <!-- Forecast Results & Interactive Regression Canvas -->
          <div class="prediction-hero-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start">
              <div>
                <span class="kpi-title">Projected Annual Precipitation</span>
                <div class="forecast-figure-box">
                  <div class="forecast-figure"><span id="forecastFigureVal">—</span> <span style="font-size:22px; font-weight:700; color:var(--text-muted)">mm</span></div>
                  <div class="forecast-delta" id="forecastDeltaBadge">
                    <span>—</span>
                  </div>
                </div>
                <div style="font-size:12px; color:var(--text-muted)" id="forecastContextSubtext">Loading regression estimate...</div>
              </div>
              <div id="forecastClassificationBadge" class="pill-accent pill-surplus" style="font-size:12px; padding:6px 14px">
                NORMAL BASELINE
              </div>
            </div>

            <!-- OLS Parameter Diagnostics -->
            <div class="stat-pills-row">
              <div class="stat-box">
                <div class="stat-box-title">Trend Rate (Slope)</div>
                <div class="stat-box-val" id="fSlopeVal">—</div>
                <div style="font-size:10px; color:var(--text-muted)">mm / calendar year</div>
              </div>
              <div class="stat-box">
                <div class="stat-box-title">Hist Mean (\(\bar{y}\))</div>
                <div class="stat-box-val" id="fMeanVal">—</div>
                <div style="font-size:10px; color:var(--text-muted)">Baseline average</div>
              </div>
              <div class="stat-box">
                <div class="stat-box-title">Model Goodness (\(R^2\))</div>
                <div class="stat-box-val" id="fR2Val">—</div>
                <div style="font-size:10px; color:var(--text-muted)">Coefficient of det.</div>
              </div>
            </div>

            <!-- Interactive Chart -->
            <div class="chart-box large"><canvas id="forecastChart"></canvas></div>
          </div>
        </div>
      </section>

      <!-- ================= SECTION 4: ANOMALY & RISK ================= -->
      <section class="page-section" id="risk">
        <div class="page-header">
          <div>
            <h1>Meteorological Anomaly & Extreme Risk Detection</h1>
            <p>Categorization of historical surplus and drought years against local climatological baselines.</p>
          </div>
          <div class="hover-hud">Threshold: Surplus &gt; +10% · Deficit &lt; −10%</div>
        </div>

        <!-- 4 Anomaly KPI Cards -->
        <div class="grid-4">
          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">Excess Surplus Years</span>
              <span class="pill-accent pill-surplus">&gt; +10%</span>
            </div>
            <div class="kpi-value" id="riskWetYears">—</div>
            <div class="kpi-footer">High flood & reservoir risk years</div>
          </div>

          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">Normal Baseline Years</span>
              <span class="pill-accent pill-primary">±10% Band</span>
            </div>
            <div class="kpi-value" id="riskNormalYears">—</div>
            <div class="kpi-footer">Within normal climatic variability</div>
          </div>

          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">Deficit / Drought Years</span>
              <span class="pill-accent pill-danger">&lt; −10%</span>
            </div>
            <div class="kpi-value" id="riskDryYears">—</div>
            <div class="kpi-footer">Agricultural drought / shortfall years</div>
          </div>

          <div class="card kpi-card">
            <div class="kpi-card-header">
              <span class="kpi-title">Historic Peak Anomaly</span>
              <span class="pill-accent pill-warning" id="riskMaxYearPill">Year</span>
            </div>
            <div class="kpi-value" id="riskMaxAnomaly">—</div>
            <div class="kpi-footer" id="riskMaxMeta">Deviation from 115y mean</div>
          </div>
        </div>

        <div class="grid-2">
          <!-- National Anomaly Diverging Bar Chart -->
          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">National Annual Rainfall Anomaly (1901–2015)</div>
                <div class="panel-subtitle">Green: Surplus (&gt; +10%), Amber: Normal, Red: Deficit (&lt; −10%)</div>
              </div>
              <div class="hover-hud" id="anomChartHud">Hover bar to inspect anomaly</div>
            </div>
            <div class="chart-box"><canvas id="anomChart"></canvas></div>
          </div>

          <!-- Extreme Years Table -->
          <div class="card panel">
            <div class="panel-header">
              <div>
                <div class="panel-title">Historic National Extreme Years</div>
                <div class="panel-subtitle">Highest surplus vs deepest recorded deficits</div>
              </div>
              <span class="pill-accent pill-primary">Top 10 Extremes</span>
            </div>
            <div class="table-wrapper">
              <table class="data-table" id="extremeTable">
                <thead>
                  <tr>
                    <th>Year</th>
                    <th>Annual Rainfall</th>
                    <th>Anomaly</th>
                    <th>Risk Classification</th>
                  </tr>
                </thead>
                <tbody id="extremeTableBody"></tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- ================= SECTION 5: DATA EXPLORER ================= -->
      <section class="page-section" id="explorer">
        <div class="page-header">
          <div>
            <h1>Comprehensive Data Explorer</h1>
            <p>Instantaneous zero-click inspection across all 4,116 subdivision records and 641 district normals.</p>
          </div>
          <div class="hover-hud" id="explorerRecordCountHud">4,757 Records Indexed</div>
        </div>

        <div class="card panel">
          <!-- Toolbar -->
          <div class="table-toolbar">
            <div class="search-input-box">
              <span class="search-icon-inside">🔍</span>
              <input type="text" id="explorerSearchInput" class="search-input" placeholder="Search state, district, subdivision, or year...">
            </div>

            <!-- Quick Filter Chips -->
            <div class="chip-bar" id="explorerFilterChips" style="margin-bottom:0">
              <span class="hover-chip active" data-filter="all">All Records</span>
              <span class="hover-chip" data-filter="historical">Subdivision Annuals (4,116)</span>
              <span class="hover-chip" data-filter="district">District Normals (641)</span>
              <span class="hover-chip" data-filter="surplus">Surplus Rainfall (&gt;2,000 mm)</span>
              <span class="hover-chip" data-filter="arid">Arid Regions (&lt;600 mm)</span>
            </div>
          </div>

          <!-- Table Wrapper -->
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Classification</th>
                  <th>Territory / Location</th>
                  <th>Year</th>
                  <th>Annual Rainfall</th>
                  <th>Monsoon (Jun–Sep)</th>
                  <th>Monsoon Ratio</th>
                  <th>Dataset Source</th>
                </tr>
              </thead>
              <tbody id="explorerTableBody"></tbody>
            </table>
          </div>

          <!-- Zero-Click Table Row Telemetry Live Inspector -->
          <div class="row-inspector-card" id="rowInspectorBox">
            <div style="display:flex; align-items:center; gap:12px">
              <span class="pill-accent pill-primary" id="inspectorType">INSPECTOR</span>
              <div>
                <strong id="inspectorLocation" style="color:var(--text-main); font-size:13px">Hover any row above for instant zero-click telemetry</strong>
                <div style="font-size:11px; color:var(--text-muted)" id="inspectorMeta">Detailed 12-month precipitation curve & status breakdown</div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:18px">
              <div style="text-align:right">
                <div style="font-size:10px; color:var(--text-muted); font-weight:700">ANNUAL RAIN</div>
                <strong style="font-size:14px; color:var(--color-primary-light)" id="inspectorAnnual">—</strong>
              </div>
              <!-- 12-month sparkline bar display -->
              <div class="sparkline-container" id="inspectorSparkline"></div>
            </div>
          </div>

          <!-- Pagination Bar -->
          <div class="pagination-container">
            <div id="explorerPaginationInfo">Showing 1–15 of 4,757 records</div>
            <div class="page-chip-list" id="explorerPaginationList"></div>
          </div>
        </div>
      </section>

    </div>
  </main>
</div>

<!-- EMBEDDED DATASET -->
<script src="data.js"></script>
<script>
// If data.js is not loaded from disk, provide fallback or validation
if (typeof DATA === 'undefined') {
  console.error("DATA object not found. Ensure data.js is in the same directory.");
}

// -------------------------------------------------------------
// CORE STATE & ZERO-CLICK ENGINE
// -------------------------------------------------------------
const MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const SEASON_NAMES = ["Winter (Jan–Feb)", "Pre-Monsoon (Mar–May)", "Monsoon (Jun–Sep)", "Post-Monsoon (Oct–Dec)"];

const state = {
  theme: localStorage.getItem("rainfall_theme") || "light",
  activeSection: "overview",
  analyticsSub: "ANDAMAN & NICOBAR ISLANDS",
  analyticsYear: "all",
  forecastSub: "ANDAMAN & NICOBAR ISLANDS",
  forecastYear: 2026,
  forecastWindow: "all",
  explorerFilter: "all",
  explorerSearch: "",
  explorerPage: 1,
  explorerPageSize: 15,
  charts: {}
};

// Formatting helpers
function fmt(n, decimals = 0) {
  if (n === null || n === undefined || isNaN(n)) return "—";
  return Number(n).toLocaleString("en-IN", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
}

function mean(arr) {
  if (!arr || !arr.length) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function stdDev(arr, m) {
  if (!arr || arr.length < 2) return 0;
  const avg = m !== undefined ? m : mean(arr);
  const variance = arr.reduce((sum, v) => sum + Math.pow(v - avg, 2), 0) / (arr.length - 1);
  return Math.sqrt(variance);
}

// Color getters based on active theme
function getThemeColors() {
  const isDark = document.body.classList.contains("theme-dark");
  const isNight = document.body.classList.contains("theme-night");
  return {
    primary: isDark ? "#3b82f6" : "#1D4ED8",
    surplus: "#10B981",
    warning: "#F59E0B",
    danger: "#EF4444",
    grid: isDark ? "rgba(255, 255, 255, 0.08)" : isNight ? "rgba(255, 255, 255, 0.09)" : "rgba(15, 23, 42, 0.08)",
    text: isDark ? "#9ca3af" : isNight ? "#94a3b8" : "#64748b",
    tooltipBg: isDark ? "#111827" : isNight ? "#1e293b" : "#ffffff",
    tooltipText: isDark ? "#f9fafb" : isNight ? "#f8fafc" : "#0f172a"
  };
}

// Chart.js helper with cleanup
function destroyChart(key) {
  if (state.charts[key]) {
    state.charts[key].destroy();
    delete state.charts[key];
  }
}

// Base chart options tuned for speed (< 100ms) and functional elegance
function getBaseChartOptions(customTooltipCallback) {
  const colors = getThemeColors();
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 180 },
    interaction: {
      mode: 'index',
      intersect: false
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        enabled: true,
        backgroundColor: colors.tooltipBg,
        titleColor: colors.tooltipText,
        bodyColor: colors.tooltipText,
        borderColor: colors.grid,
        borderWidth: 1,
        padding: 9,
        cornerRadius: 6,
        displayColors: false,
        titleFont: { family: 'Inter', weight: '700', size: 11 },
        bodyFont: { family: 'Inter', size: 11 },
        callbacks: customTooltipCallback || {}
      }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { color: colors.text, font: { family: 'Inter', size: 10 } }
      },
      y: {
        grid: { color: colors.grid },
        ticks: { color: colors.text, font: { family: 'Inter', size: 10 } }
      }
    }
  };
}

// -------------------------------------------------------------
// 1. OVERVIEW MODULE
// -------------------------------------------------------------
function initOverviewModule() {
  const annuals = DATA.annual.filter(r => r.a > 0);
  const overallAvg = mean(annuals.map(r => r.a));
  document.getElementById("kpiAvgValue").textContent = fmt(overallAvg, 1);

  // Group by subdivision to find wettest & driest
  const subMap = {};
  annuals.forEach(r => {
    (subMap[r.s] ??= []).push(r.a);
  });
  const subStats = Object.entries(subMap).map(([s, vals]) => ({
    name: s,
    avg: mean(vals)
  })).sort((a, b) => b.avg - a.avg);

  const wettest = subStats[0];
  const driest = subStats[subStats.length - 1];

  document.getElementById("kpiWetName").textContent = wettest.name;
  document.getElementById("kpiWetAnnual").textContent = fmt(wettest.avg, 0) + " mm";
  document.getElementById("kpiDryName").textContent = driest.name;
  document.getElementById("kpiDryAnnual").textContent = fmt(driest.avg, 0) + " mm";

  // Monsoon share
  const monsoonPercentages = annuals.map(r => (r.se[2] / r.a) * 100).filter(v => !isNaN(v) && isFinite(v));
  const avgMonsoonShare = mean(monsoonPercentages);
  document.getElementById("kpiMonsoonShare").textContent = fmt(avgMonsoonShare, 1);

  // National Annual Series for Trend Line & OLS
  const yearMap = {};
  annuals.forEach(r => {
    (yearMap[r.y] ??= []).push(r.a);
  });
  const nationalSeries = Object.entries(yearMap).map(([y, vals]) => ({
    year: +y,
    annual: mean(vals)
  })).sort((a, b) => a.year - b.year);

  // Calculate national OLS trend
  const xs = nationalSeries.map(r => r.year);
  const ys = nationalSeries.map(r => r.annual);
  const xm = mean(xs);
  const ym = mean(ys);
  const num = xs.reduce((acc, x, i) => acc + (x - xm) * (ys[i] - ym), 0);
  const den = xs.reduce((acc, x) => acc + Math.pow(x - xm, 2), 0);
  const slope = den !== 0 ? num / den : 0;
  const intercept = ym - slope * xm;
  const trendLine = xs.map(x => intercept + slope * x);

  // Render Trend Chart
  destroyChart("trendChart");
  const colors = getThemeColors();
  const trendOpts = getBaseChartOptions({
    title: (items) => `Year: ${items[0].label}`,
    label: (ctx) => `Annual Rain: ${fmt(ctx.parsed.y, 1)} mm`,
    afterLabel: (ctx) => {
      const dev = ((ctx.parsed.y - overallAvg) / overallAvg) * 100;
      return `Anomaly: ${dev >= 0 ? '+' : ''}${dev.toFixed(1)}% vs baseline`;
    }
  });

  const ctxTrend = document.getElementById("trendChart").getContext("2d");
  state.charts.trendChart = new Chart(ctxTrend, {
    type: 'line',
    data: {
      labels: xs,
      datasets: [
        {
          label: "National Annual Average",
          data: ys,
          borderColor: colors.primary,
          backgroundColor: "rgba(29, 78, 216, 0.08)",
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: colors.primary,
          fill: true,
          tension: 0.2
        },
        {
          label: "OLS Secular Trend",
          data: trendLine,
          borderColor: colors.warning,
          borderWidth: 2,
          borderDash: [5, 4],
          pointRadius: 0,
          fill: false,
          tension: 0
        }
      ]
    },
    options: {
      ...trendOpts,
      onHover: (e, activeElements) => {
        if (activeElements && activeElements.length) {
          const idx = activeElements[0].index;
          const year = xs[idx];
          const val = ys[idx];
          const dev = ((val - overallAvg) / overallAvg) * 100;
          document.getElementById("trendHoverHud").innerHTML = `Year <strong>${year}</strong>: <strong>${fmt(val, 1)} mm</strong> (${dev >= 0 ? '+' : ''}${dev.toFixed(1)}%)`;
        }
      }
    }
  });

  // Top 10 Subdivision Leaderboard (Zero-Click Interactive Rows)
  const top10 = subStats.slice(0, 10);
  const maxSubAvg = top10[0].avg;
  const rankListEl = document.getElementById("overviewRankList");
  rankListEl.innerHTML = top10.map((item, i) => `
    <div class="rank-row hover-snap" data-sub="${item.name}">
      <div class="rank-num">${i + 1}</div>
      <div>
        <div class="rank-name">${item.name}</div>
        <div class="rank-bar-bg"><div class="rank-bar-fill" style="width:${Math.max(8, (item.avg / maxSubAvg) * 100)}%"></div></div>
      </div>
      <div class="rank-val">${fmt(item.avg, 0)} mm</div>
    </div>
  `).join("");

  // Attach zero-click hover to rank rows
  rankListEl.querySelectorAll(".rank-row").forEach(row => {
    row.addEventListener("mouseenter", () => {
      const subName = row.dataset.sub;
      document.getElementById("trendHoverHud").innerHTML = `Region: <strong>${subName}</strong>`;
    });
  });

  // Monthly Chart
  const monthlyMeans = MONTH_NAMES.map((_, mIdx) => mean(annuals.map(r => r.m[mIdx])));
  destroyChart("monthlyChart");
  const ctxMonthly = document.getElementById("monthlyChart").getContext("2d");
  state.charts.monthlyChart = new Chart(ctxMonthly, {
    type: 'bar',
    data: {
      labels: MONTH_NAMES,
      datasets: [{
        label: "National Mean",
        data: monthlyMeans,
        backgroundColor: monthlyMeans.map(v => v > 200 ? colors.surplus : v > 80 ? colors.primary : colors.warning),
        borderRadius: 4
      }]
    },
    options: getBaseChartOptions({
      label: (ctx) => `Rainfall: ${fmt(ctx.parsed.y, 1)} mm`
    })
  });

  // Seasonal Chart
  const seasonalMeans = SEASON_NAMES.map((_, sIdx) => mean(annuals.map(r => r.se[sIdx])));
  destroyChart("seasonalChart");
  const ctxSeasonal = document.getElementById("seasonalChart").getContext("2d");
  state.charts.seasonalChart = new Chart(ctxSeasonal, {
    type: 'bar',
    data: {
      labels: ["Winter", "Pre-Monsoon", "Monsoon (SW)", "Post-Monsoon"],
      datasets: [{
        label: "Season Mean",
        data: seasonalMeans,
        backgroundColor: [colors.warning, colors.primary, colors.surplus, colors.warning],
        borderRadius: 5
      }]
    },
    options: getBaseChartOptions({
      label: (ctx) => `${ctx.dataset.label}: ${fmt(ctx.parsed.y, 1)} mm`
    })
  });

  // Insights
  const insightsContainer = document.getElementById("overviewInsights");
  const first20Y = mean(nationalSeries.slice(0, 20).map(r => r.annual));
  const last20Y = mean(nationalSeries.slice(-20).map(r => r.annual));
  const shiftPct = ((last20Y - first20Y) / first20Y) * 100;

  insightsContainer.innerHTML = `
    <div class="insight-item">
      <strong><span class="insight-dot"></span>Monsoon Concentration</strong>
      <span>SW Monsoon (Jun–Sep) delivers <b>${fmt(avgMonsoonShare, 0)}%</b> of India's annual precipitation budget.</span>
    </div>
    <div class="insight-item">
      <strong><span class="insight-dot"></span>Extreme Regional Disparity</strong>
      <span>Ratio between wettest (${wettest.name.split(' ')[0]}) and driest is over <b>${fmt(wettest.avg / driest.avg, 1)}x</b>.</span>
    </div>
    <div class="insight-item">
      <strong><span class="insight-dot"></span>Centurial Trend (${shiftPct >= 0 ? '+' : ''}${fmt(shiftPct, 1)}%)</strong>
      <span>Initial 20-year mean was <b>${fmt(first20Y, 0)} mm</b> vs <b>${fmt(last20Y, 0)} mm</b> in the final 20 years.</span>
    </div>
    <div class="insight-item">
      <strong><span class="insight-dot" style="background:var(--color-warning)"></span>Analytical Context</strong>
      <span>High variance in arid zones emphasizes adaptive water stewardship across sub-basins.</span>
    </div>
  `;
}

// -------------------------------------------------------------
// 2. ANALYTICS MODULE (Zero-Click Parameter Hover)
// -------------------------------------------------------------
function initAnalyticsModule() {
  const subDropdown = document.getElementById("analyticsSubDropdown");
  const yearDropdown = document.getElementById("analyticsYearDropdown");
  const subChips = document.getElementById("analyticsSubChips");

  // Populate Subdivision Dropdown (Hover-to-select)
  subDropdown.innerHTML = DATA.subs.map(s => `
    <div class="hover-dropdown-item ${s === state.analyticsSub ? 'selected' : ''}" data-value="${s}">
      <span>${s}</span>
    </div>
  `).join("");

  // Populate Quick Chips (First 8 major subdivisions)
  const quickSubs = DATA.subs.slice(0, 10);
  subChips.innerHTML = quickSubs.map(s => `
    <span class="hover-chip ${s === state.analyticsSub ? 'active' : ''}" data-value="${s}">${s}</span>
  `).join("");

  // Populate Year Dropdown
  const yearOptions = [`<div class="hover-dropdown-item selected" data-value="all">115-Year Historical Average</div>`].concat(
    DATA.years.map(y => `<div class="hover-dropdown-item" data-value="${y}">${y}</div>`)
  );
  yearDropdown.innerHTML = yearOptions.join("");

  // Zero-click hover listeners on subdivision items
  subDropdown.querySelectorAll(".hover-dropdown-item").forEach(item => {
    item.addEventListener("mouseenter", () => {
      setAnalyticsSubdivision(item.dataset.value);
    });
  });

  subChips.querySelectorAll(".hover-chip").forEach(chip => {
    chip.addEventListener("mouseenter", () => {
      setAnalyticsSubdivision(chip.dataset.value);
    });
  });

  // Zero-click hover listeners on year items
  yearDropdown.querySelectorAll(".hover-dropdown-item").forEach(item => {
    item.addEventListener("mouseenter", () => {
      setAnalyticsYear(item.dataset.value);
    });
  });

  // Reset button
  document.getElementById("analyticsResetBtn").addEventListener("mouseenter", () => {
    setAnalyticsSubdivision(DATA.subs[0]);
    setAnalyticsYear("all");
  });

  // Districts Leaderboard (From 641 District Normals dataset)
  const sortedDistricts = [...DATA.district].sort((a, b) => b.a - a.a);
  const maxDist = sortedDistricts[0].a;
  const wetDistricts = sortedDistricts.slice(0, 8);
  const dryDistricts = [...sortedDistricts].reverse().slice(0, 8);

  const renderDistrictList = (targetId, list, isWet) => {
    document.getElementById(targetId).innerHTML = list.map((d, i) => `
      <div class="rank-row hover-snap" data-dist="${d.d}" data-state="${d.st}" data-rain="${d.a}">
        <div class="rank-num">${i + 1}</div>
        <div>
          <div class="rank-name">${d.d}</div>
          <div style="font-size:10px; color:var(--text-muted)">${d.st}</div>
          <div class="rank-bar-bg"><div class="rank-bar-fill" style="width:${(d.a / maxDist) * 100}%; background:${isWet ? 'var(--color-surplus)' : 'var(--color-danger)'}"></div></div>
        </div>
        <div class="rank-val">${fmt(d.a, 0)} mm</div>
      </div>
    `).join("");
  };

  renderDistrictList("wetDistrictsList", wetDistricts, true);
  renderDistrictList("dryDistrictsList", dryDistricts, false);

  // Zero-click hover telemetry on district rows
  document.querySelectorAll("#wetDistrictsList .rank-row, #dryDistrictsList .rank-row").forEach(row => {
    row.addEventListener("mouseenter", () => {
      document.getElementById("analyticsHud").innerHTML = `District: <strong>${row.dataset.dist} (${row.dataset.state})</strong> · Normal: <strong>${fmt(row.dataset.rain, 0)} mm</strong>`;
    });
  });

  renderAnalyticsCharts();
}

function setAnalyticsSubdivision(subName) {
  state.analyticsSub = subName;
  document.getElementById("analyticsSubLabel").textContent = subName;

  // Update active chips and dropdown highlight
  document.querySelectorAll("#analyticsSubDropdown .hover-dropdown-item").forEach(el => {
    el.classList.toggle("selected", el.dataset.value === subName);
  });
  document.querySelectorAll("#analyticsSubChips .hover-chip").forEach(el => {
    el.classList.toggle("active", el.dataset.value === subName);
  });

  renderAnalyticsCharts();
}

function setAnalyticsYear(yearVal) {
  state.analyticsYear = yearVal;
  document.getElementById("analyticsYearLabel").textContent = yearVal === "all" ? "115-Year Historical Average" : `Calendar Year ${yearVal}`;

  document.querySelectorAll("#analyticsYearDropdown .hover-dropdown-item").forEach(el => {
    el.classList.toggle("selected", el.dataset.value === yearVal);
  });

  renderAnalyticsCharts();
}

function renderAnalyticsCharts() {
  const rows = DATA.annual.filter(r => r.s === state.analyticsSub && r.a > 0);
  if (!rows.length) return;

  let monthlyData, seasonalData, meanAnnual;
  if (state.analyticsYear === "all") {
    monthlyData = MONTH_NAMES.map((_, i) => mean(rows.map(r => r.m[i])));
    seasonalData = [0, 1, 2, 3].map(i => mean(rows.map(r => r.se[i])));
    meanAnnual = mean(rows.map(r => r.a));
  } else {
    const yr = +state.analyticsYear;
    const match = rows.find(r => r.y === yr) || rows[0];
    monthlyData = match.m;
    seasonalData = match.se;
    meanAnnual = match.a;
  }

  document.getElementById("analyticsSubStatPill").textContent = `${state.analyticsSub} (${fmt(meanAnnual, 1)} mm)`;

  const colors = getThemeColors();

  // Monthly chart
  destroyChart("analyticsMonthlyChart");
  const ctxMonthly = document.getElementById("analyticsMonthlyChart").getContext("2d");
  state.charts.analyticsMonthlyChart = new Chart(ctxMonthly, {
    type: 'bar',
    data: {
      labels: MONTH_NAMES,
      datasets: [{
        label: "Rainfall",
        data: monthlyData,
        backgroundColor: colors.primary,
        hoverBackgroundColor: colors.primary,
        borderRadius: 4
      }]
    },
    options: getBaseChartOptions({
      label: (ctx) => `Precipitation: ${fmt(ctx.parsed.y, 1)} mm`
    })
  });

  // Seasonal chart
  destroyChart("analyticsSeasonalChart");
  const ctxSeasonal = document.getElementById("analyticsSeasonalChart").getContext("2d");
  state.charts.analyticsSeasonalChart = new Chart(ctxSeasonal, {
    type: 'bar',
    data: {
      labels: ["Jan–Feb", "Mar–May", "Jun–Sep", "Oct–Dec"],
      datasets: [{
        label: "Season Volume",
        data: seasonalData,
        backgroundColor: [colors.warning, colors.primary, colors.surplus, colors.warning],
        borderRadius: 4
      }]
    },
    options: getBaseChartOptions({
      label: (ctx) => `Volume: ${fmt(ctx.parsed.y, 1)} mm`
    })
  });
}

// -------------------------------------------------------------
// 3. PREDICTION & OLS REGRESSION MODULE (Zero-Click Parameter Hover)
// -------------------------------------------------------------
function initForecastModule() {
  const subDropdown = document.getElementById("forecastSubDropdown");
  subDropdown.innerHTML = DATA.subs.map(s => `
    <div class="hover-dropdown-item ${s === state.forecastSub ? 'selected' : ''}" data-value="${s}">
      <span>${s}</span>
    </div>
  `).join("");

  subDropdown.querySelectorAll(".hover-dropdown-item").forEach(item => {
    item.addEventListener("mouseenter", () => {
      setForecastSubdivision(item.dataset.value);
    });
  });

  // Year hover chips
  document.querySelectorAll("#forecastYearChips .hover-chip").forEach(chip => {
    chip.addEventListener("mouseenter", () => {
      setForecastYear(+chip.dataset.year);
    });
  });

  // Slider change
  const slider = document.getElementById("forecastYearSlider");
  slider.addEventListener("input", (e) => {
    setForecastYear(+e.target.value);
  });

  // Baseline window chips (Hover-activated parameter sensitivity)
  document.querySelectorAll("#baselineWindowChips .hover-chip").forEach(chip => {
    chip.addEventListener("mouseenter", () => {
      document.querySelectorAll("#baselineWindowChips .hover-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      state.forecastWindow = chip.dataset.window;
      runOLSForecast();
    });
  });

  runOLSForecast();
}

function setForecastSubdivision(subName) {
  state.forecastSub = subName;
  document.getElementById("forecastSubLabel").textContent = subName;
  document.querySelectorAll("#forecastSubDropdown .hover-dropdown-item").forEach(el => {
    el.classList.toggle("selected", el.dataset.value === subName);
  });
  runOLSForecast();
}

function setForecastYear(year) {
  state.forecastYear = year;
  document.getElementById("forecastYearBadge").textContent = year;
  document.getElementById("forecastYearSlider").value = year;
  document.querySelectorAll("#forecastYearChips .hover-chip").forEach(el => {
    el.classList.toggle("active", +el.dataset.year === year);
  });
  runOLSForecast();
}

// Full OLS Linear Regression Computation Engine
function runOLSForecast() {
  let rows = DATA.annual.filter(r => r.s === state.forecastSub && r.a > 0).sort((a, b) => a.y - b.y);
  if (state.forecastWindow === "1950") {
    rows = rows.filter(r => r.y >= 1950);
  } else if (state.forecastWindow === "1980") {
    rows = rows.filter(r => r.y >= 1980);
  }
  if (!rows.length) return;

  const n = rows.length;
  const xs = rows.map(r => r.y);
  const ys = rows.map(r => r.a);

  const xMean = mean(xs);
  const yMean = mean(ys);

  // OLS slope & intercept
  const num = xs.reduce((acc, x, i) => acc + (x - xMean) * (ys[i] - yMean), 0);
  const den = xs.reduce((acc, x) => acc + Math.pow(x - xMean, 2), 0);
  const slope = den !== 0 ? num / den : 0;
  const intercept = yMean - slope * xMean;

  // Coefficient of determination R^2
  const ssTot = ys.reduce((acc, y) => acc + Math.pow(y - yMean, 2), 0);
  const ssRes = rows.reduce((acc, r) => acc + Math.pow(r.a - (intercept + slope * r.y), 2), 0);
  const r2 = ssTot > 0 ? Math.max(0, 1 - (ssRes / ssTot)) : 0;

  // Prediction for target year
  const predYear = state.forecastYear;
  const predictedRain = Math.max(0, intercept + slope * predYear);
  const deltaFromMean = ((predictedRain - yMean) / yMean) * 100;

  // Update UI Figures
  document.getElementById("forecastFigureVal").textContent = fmt(predictedRain, 1);
  const deltaBadge = document.getElementById("forecastDeltaBadge");
  const isSurplus = deltaFromMean >= 0;
  deltaBadge.innerHTML = `
    <span class="pill-accent ${Math.abs(deltaFromMean) < 10 ? 'pill-primary' : isSurplus ? 'pill-surplus' : 'pill-danger'}">
      ${isSurplus ? '▲ +' : '▼ '}${fmt(deltaFromMean, 1)}%
    </span>
    <span style="color:var(--text-muted)">vs ${n}-yr historical baseline (${fmt(yMean, 0)} mm)</span>
  `;

  document.getElementById("forecastContextSubtext").textContent = `${state.forecastSub} · Target Horizon Year ${predYear}`;

  // Classification Badge
  const classBadge = document.getElementById("forecastClassificationBadge");
  if (predictedRain > yMean * 1.1) {
    classBadge.className = "pill-accent pill-surplus";
    classBadge.textContent = "ABOVE NORMAL TREND (+SURPLUS)";
  } else if (predictedRain < yMean * 0.9) {
    classBadge.className = "pill-accent pill-danger";
    classBadge.textContent = "DEFICIT TREND (BELOW BASELINE)";
  } else {
    classBadge.className = "pill-accent pill-primary";
    classBadge.textContent = "NORMAL CLIMATIC BASELINE";
  }

  // Diagnostics Box
  document.getElementById("fSlopeVal").textContent = `${slope >= 0 ? '+' : ''}${fmt(slope, 2)}`;
  document.getElementById("fMeanVal").textContent = `${fmt(yMean, 1)} mm`;
  document.getElementById("fR2Val").textContent = r2.toFixed(4);

  // Render Chart with historical line + OLS fit + predicted point
  const allYears = xs.concat([predYear]);
  const historicalPoints = ys.concat([null]);
  const fittedPoints = xs.map(x => intercept + slope * x).concat([predictedRain]);

  destroyChart("forecastChart");
  const colors = getThemeColors();
  const ctx = document.getElementById("forecastChart").getContext("2d");

  state.charts.forecastChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: allYears,
      datasets: [
        {
          label: "Historical Observed",
          data: historicalPoints,
          borderColor: colors.primary,
          backgroundColor: "rgba(29, 78, 216, 0.05)",
          borderWidth: 2,
          pointRadius: 0,
          pointHoverRadius: 5,
          tension: 0.15,
          fill: true
        },
        {
          label: "OLS Regression Baseline",
          data: fittedPoints,
          borderColor: colors.warning,
          borderWidth: 2,
          borderDash: [6, 4],
          pointRadius: allYears.map((y, i) => i === allYears.length - 1 ? 6 : 0),
          pointBackgroundColor: colors.warning,
          pointHoverRadius: 8,
          tension: 0
        }
      ]
    },
    options: {
      ...getBaseChartOptions({
        title: (items) => `Year: ${items[0].label}`,
        label: (ctx) => {
          const val = ctx.parsed.y;
          if (ctx.datasetIndex === 1 && ctx.dataIndex === allYears.length - 1) {
            return `Projected ${predYear}: ${fmt(val, 1)} mm (${deltaFromMean >= 0 ? '+' : ''}${fmt(deltaFromMean, 1)}%)`;
          }
          return `${ctx.dataset.label}: ${fmt(val, 1)} mm`;
        }
      }),
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: { font: { family: 'Inter', size: 10 }, color: colors.text }
        }
      }
    }
  });
}

// -------------------------------------------------------------
// 4. ANOMALY & RISK MODULE
// -------------------------------------------------------------
function initRiskModule() {
  const annuals = DATA.annual.filter(r => r.a > 0);
  const yearMap = {};
  annuals.forEach(r => {
    (yearMap[r.y] ??= []).push(r.a);
  });
  const nationalSeries = Object.entries(yearMap).map(([y, vals]) => ({
    year: +y,
    annual: mean(vals)
  })).sort((a, b) => a.year - b.year);

  const baseline = mean(nationalSeries.map(r => r.annual));

  let wetCount = 0, normCount = 0, dryCount = 0;
  const anomalies = nationalSeries.map(r => {
    const dev = ((r.annual - baseline) / baseline) * 100;
    if (dev > 10) wetCount++;
    else if (dev < -10) dryCount++;
    else normCount++;
    return { year: r.year, rain: r.annual, dev };
  });

  document.getElementById("riskWetYears").textContent = wetCount;
  document.getElementById("riskNormalYears").textContent = normCount;
  document.getElementById("riskDryYears").textContent = dryCount;

  // Largest absolute anomaly
  const sortedByAbs = [...anomalies].sort((a, b) => Math.abs(b.dev) - Math.abs(a.dev));
  const maxAnom = sortedByAbs[0];
  document.getElementById("riskMaxAnomaly").textContent = `${maxAnom.dev >= 0 ? '+' : ''}${fmt(maxAnom.dev, 1)}%`;
  document.getElementById("riskMaxYearPill").textContent = `Year ${maxAnom.year}`;
  document.getElementById("riskMaxMeta").textContent = `${fmt(maxAnom.rain, 1)} mm (${maxAnom.dev >= 0 ? 'Surplus Peak' : 'Deficit Peak'})`;

  // Anomaly Diverging Chart
  destroyChart("anomChart");
  const colors = getThemeColors();
  const ctxAnom = document.getElementById("anomChart").getContext("2d");

  state.charts.anomChart = new Chart(ctxAnom, {
    type: 'bar',
    data: {
      labels: anomalies.map(r => r.year),
      datasets: [{
        label: "Anomaly %",
        data: anomalies.map(r => r.dev),
        backgroundColor: anomalies.map(r => r.dev > 10 ? colors.surplus : r.dev < -10 ? colors.danger : colors.warning),
        borderRadius: 2
      }]
    },
    options: {
      ...getBaseChartOptions({
        title: (items) => `Year ${items[0].label}`,
        label: (ctx) => `Deviation: ${ctx.parsed.y >= 0 ? '+' : ''}${fmt(ctx.parsed.y, 2)}% vs baseline (${fmt(baseline, 0)} mm)`
      }),
      scales: {
        x: { grid: { display: false }, ticks: { color: colors.text, font: { size: 10 } } },
        y: {
          grid: { color: colors.grid },
          ticks: { color: colors.text, font: { size: 10 }, callback: (v) => `${v}%` }
        }
      },
      onHover: (e, activeElements) => {
        if (activeElements && activeElements.length) {
          const idx = activeElements[0].index;
          const a = anomalies[idx];
          document.getElementById("anomChartHud").innerHTML = `Year <strong>${a.year}</strong>: <strong>${a.dev >= 0 ? '+' : ''}${fmt(a.dev, 2)}%</strong> (${fmt(a.rain, 0)} mm)`;
        }
      }
    }
  });

  // Extreme Years Table Body (Top 5 wettest and top 5 driest)
  const topSurplus = [...anomalies].sort((a, b) => b.dev - a.dev).slice(0, 5);
  const topDeficits = [...anomalies].sort((a, b) => a.dev - b.dev).slice(0, 5);
  const extremes = topSurplus.concat(topDeficits);

  const tbody = document.getElementById("extremeTableBody");
  tbody.innerHTML = extremes.map(r => `
    <tr class="hover-snap" data-year="${r.year}">
      <td><strong>${r.year}</strong></td>
      <td>${fmt(r.rain, 1)} mm</td>
      <td><span class="pill-accent ${r.dev > 10 ? 'pill-surplus' : r.dev < -10 ? 'pill-danger' : 'pill-warning'}">${r.dev >= 0 ? '+' : ''}${fmt(r.dev, 1)}%</span></td>
      <td>${r.dev > 10 ? 'Extreme Rainfall / Flood Risk' : 'Severe Deficit / Drought'}</td>
    </tr>
  `).join("");

  tbody.querySelectorAll("tr").forEach(tr => {
    tr.addEventListener("mouseenter", () => {
      const yr = +tr.dataset.year;
      const match = anomalies.find(a => a.year === yr);
      if (match) {
        document.getElementById("anomChartHud").innerHTML = `Extreme Year <strong>${match.year}</strong>: <strong>${match.dev >= 0 ? '+' : ''}${fmt(match.dev, 2)}%</strong>`;
      }
    });
  });
}

// -------------------------------------------------------------
// 5. DATA EXPLORER MODULE (Zero-Click Hover Telemetry)
// -------------------------------------------------------------
let allRecordsCache = [];
let filteredRecordsCache = [];

function initExplorerModule() {
  // Build unified search cache
  const histRecords = DATA.annual.filter(r => r.a > 0).map(r => ({
    type: "Subdivision Annual",
    loc: r.s,
    year: r.y,
    annual: r.a,
    monsoon: r.se[2],
    monsoonRatio: r.a > 0 ? (r.se[2] / r.a) * 100 : 0,
    m: r.m,
    src: "IMD 115-Year Archive"
  }));

  const distRecords = DATA.district.filter(r => r.a > 0).map(r => ({
    type: "District Normal",
    loc: `${r.d}, ${r.st}`,
    year: "Normal",
    annual: r.a,
    monsoon: r.m.slice(5, 9).reduce((a, b) => a + b, 0),
    monsoonRatio: r.a > 0 ? ((r.m.slice(5, 9).reduce((a, b) => a + b, 0)) / r.a) * 100 : 0,
    m: r.m,
    src: "District Normal Norms"
  }));

  allRecordsCache = histRecords.concat(distRecords);
  filteredRecordsCache = allRecordsCache;

  // Search input event
  const searchInput = document.getElementById("explorerSearchInput");
  searchInput.addEventListener("input", (e) => {
    state.explorerSearch = e.target.value.toLowerCase().trim();
    state.explorerPage = 1;
    filterAndRenderExplorer();
  });

  // Filter chips (Hover-activated)
  document.querySelectorAll("#explorerFilterChips .hover-chip").forEach(chip => {
    chip.addEventListener("mouseenter", () => {
      document.querySelectorAll("#explorerFilterChips .hover-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      state.explorerFilter = chip.dataset.filter;
      state.explorerPage = 1;
      filterAndRenderExplorer();
    });
  });

  filterAndRenderExplorer();
}

function filterAndRenderExplorer() {
  const q = state.explorerSearch;
  const filter = state.explorerFilter;

  filteredRecordsCache = allRecordsCache.filter(r => {
    // Text search
    const matchesSearch = !q || (r.loc + " " + r.year + " " + r.type).toLowerCase().includes(q);
    if (!matchesSearch) return false;

    // Categorical filter
    if (filter === "historical") return r.type === "Subdivision Annual";
    if (filter === "district") return r.type === "District Normal";
    if (filter === "surplus") return r.annual >= 2000;
    if (filter === "arid") return r.annual <= 600;
    return true;
  });

  renderExplorerTable();
}

function renderExplorerTable() {
  const total = filteredRecordsCache.length;
  const totalPages = Math.max(1, Math.ceil(total / state.explorerPageSize));
  state.explorerPage = Math.min(state.explorerPage, totalPages);

  const startIdx = (state.explorerPage - 1) * state.explorerPageSize;
  const endIdx = Math.min(startIdx + state.explorerPageSize, total);
  const pageRows = filteredRecordsCache.slice(startIdx, endIdx);

  const tbody = document.getElementById("explorerTableBody");
  if (!pageRows.length) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--text-muted)">No matching records found.</td></tr>`;
    document.getElementById("explorerPaginationInfo").textContent = "0 matching records";
    document.getElementById("explorerPaginationList").innerHTML = "";
    return;
  }

  tbody.innerHTML = pageRows.map((r, idx) => `
    <tr class="hover-snap" data-idx="${startIdx + idx}">
      <td><span class="pill-accent ${r.type.includes('Subdivision') ? 'pill-primary' : 'pill-surplus'}" style="font-size:10px">${r.type}</span></td>
      <td><strong>${r.loc}</strong></td>
      <td>${r.year}</td>
      <td><strong>${fmt(r.annual, 1)}</strong> mm</td>
      <td>${fmt(r.monsoon, 1)} mm</td>
      <td>${fmt(r.monsoonRatio, 1)}%</td>
      <td style="color:var(--text-muted); font-size:11px">${r.src}</td>
    </tr>
  `).join("");

  document.getElementById("explorerPaginationInfo").textContent = `Showing ${startIdx + 1}–${endIdx} of ${fmt(total)} records`;

  // Zero-click table row hover: instantaneous telemetry update
  tbody.querySelectorAll("tr").forEach(tr => {
    tr.addEventListener("mouseenter", () => {
      const record = filteredRecordsCache[+tr.dataset.idx];
      if (record) updateRowInspector(record);
    });
  });

  // Render first item to inspector initially
  if (pageRows.length) updateRowInspector(pageRows[0]);

  // Render Zero-Click Hover Pagination Chips
  renderHoverPagination(totalPages);
}

// Live Row Inspector
function updateRowInspector(record) {
  document.getElementById("inspectorType").textContent = record.type.toUpperCase();
  document.getElementById("inspectorLocation").textContent = `${record.loc} (${record.year})`;
  document.getElementById("inspectorAnnual").textContent = `${fmt(record.annual, 1)} mm`;
  document.getElementById("inspectorMeta").textContent = `SW Monsoon: ${fmt(record.monsoon, 1)} mm (${fmt(record.monsoonRatio, 1)}% contribution) · Source: ${record.src}`;

  // Build sparkline bars for 12 months
  const sparkContainer = document.getElementById("inspectorSparkline");
  const maxM = Math.max(1, ...record.m);
  sparkContainer.innerHTML = record.m.map((val, i) => `
    <div class="spark-bar" title="${MONTH_NAMES[i]}: ${val} mm" style="height:${Math.max(3, (val / maxM) * 26)}px; background:${val > 250 ? 'var(--color-surplus)' : val > 100 ? 'var(--color-primary-light)' : 'var(--border-hover)'}"></div>
  `).join("");
}

// Zero-Click Hover Pagination
function renderHoverPagination(totalPages) {
  const container = document.getElementById("explorerPaginationList");
  let pages = [];
  const current = state.explorerPage;

  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    pages.push(1);
    if (current > 3) pages.push("...");
    for (let i = Math.max(2, current - 1); i <= Math.min(totalPages - 1, current + 1); i++) {
      pages.push(i);
    }
    if (current < totalPages - 2) pages.push("...");
    pages.push(totalPages);
  }

  container.innerHTML = pages.map(p => `
    <span class="page-chip ${p === current ? 'active' : ''} ${p === '...' ? 'disabled' : ''}" data-page="${p}">${p}</span>
  `).join("");

  // Attach zero-click hover to pagination chips
  container.querySelectorAll(".page-chip:not(.disabled)").forEach(chip => {
    let hoverTimeout = null;
    chip.addEventListener("mouseenter", () => {
      // 120ms debounce so it doesn't trigger wildly when sweeping cursor across
      hoverTimeout = setTimeout(() => {
        state.explorerPage = +chip.dataset.page;
        renderExplorerTable();
      }, 120);
    });
    chip.addEventListener("mouseleave", () => {
      if (hoverTimeout) clearTimeout(hoverTimeout);
    });
    // Click fallback for accessibility
    chip.addEventListener("click", () => {
      state.explorerPage = +chip.dataset.page;
      renderExplorerTable();
    });
  });
}

// -------------------------------------------------------------
// 6. ZERO-CLICK SECTION NAVIGATION CONTROLLER (Strict Requirement)
// -------------------------------------------------------------
function initNavigation() {
  const navButtons = document.querySelectorAll("#mainNav .nav-btn");
  const sections = document.querySelectorAll(".page-section");
  const badge = document.getElementById("activeSectionBadge");

  function activateSection(targetId) {
    if (state.activeSection === targetId) return;
    state.activeSection = targetId;

    // Update nav button active states
    navButtons.forEach(btn => {
      btn.classList.toggle("active", btn.dataset.target === targetId);
    });

    // Update visible section
    sections.forEach(sec => {
      sec.classList.toggle("active", sec.id === targetId);
    });

    // Update topbar badge
    badge.textContent = targetId.toUpperCase();

    // Trigger chart resize/re-render for proper container dimensions
    setTimeout(() => {
      Object.values(state.charts).forEach(ch => {
        if (ch && typeof ch.resize === 'function') ch.resize();
      });
    }, 40);
  }

  // Strict Rule: Mouseenter immediately switches tab without clicking
  navButtons.forEach(btn => {
    btn.addEventListener("mouseenter", () => {
      activateSection(btn.dataset.target);
    });
    // Keyboard focus support
    btn.addEventListener("focus", () => {
      activateSection(btn.dataset.target);
    });
  });
}

// -------------------------------------------------------------
// 7. THEME SYSTEM
// -------------------------------------------------------------
function applyTheme(themeName) {
  state.theme = themeName;
  document.body.classList.remove("theme-night", "theme-dark");
  if (themeName === "night") document.body.classList.add("theme-night");
  if (themeName === "dark") document.body.classList.add("theme-dark");

  document.querySelectorAll(".theme-pill-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.theme === themeName);
  });

  localStorage.setItem("rainfall_theme", themeName);

  // Re-render charts so colors adapt
  initOverviewModule();
  renderAnalyticsCharts();
  runOLSForecast();
  initRiskModule();
}

function initThemeSwitcher() {
  document.querySelectorAll(".theme-pill-btn").forEach(btn => {
    // Hover switches theme instantly
    btn.addEventListener("mouseenter", () => {
      applyTheme(btn.dataset.theme);
    });
  });
}

// -------------------------------------------------------------
// DOM INITIALIZATION
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  // Apply saved theme
  applyTheme(state.theme);

  // Initialize Navigation
  initNavigation();

  // Initialize Theme Switcher
  initThemeSwitcher();

  // Initialize Modules
  initOverviewModule();
  initAnalyticsModule();
  initForecastModule();
  initRiskModule();
  initExplorerModule();

  console.log("Rainfall Intelligence Dashboard initialized with Zero-Click Hover Navigation.");
});
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Successfully wrote redesigned index.html!")
