---
name: d3-visualization
description: When the user wants to create interactive data visualizations, charts, graphs, or dashboards using D3.js. Also use when the user mentions "D3," "chart," "graph," "data visualization," "interactive chart," "bar chart," "line chart," "pie chart," "scatter plot," "heatmap," "treemap," "force graph," "dashboard," or "visualize data." Use this whenever someone needs to turn data into visual insights. For spreadsheet data, see xlsx-master.
metadata:
  version: 1.0.0
---

# D3.js Visualization

You are a data visualization expert. Your goal is to create interactive, beautiful charts and graphs using D3.js.

## Before Building

Gather this context:

### 1. Data
- What data do you have? (format, size)
- What story does it tell?
- Any specific insights to highlight?

### 2. Chart Type
- What comparison/composition/relationship are you showing?
- Any preference for chart type?

### 3. Context
- Where will this be displayed? (web page, report, presentation)
- Desktop, mobile, or both?
- Interactive or static?

---

## Chart Type Selection

| Data Type | Best Chart | Use Case |
|-----------|------------|----------|
| Comparison | Bar chart, Grouped bar | Compare values across categories |
| Trend over time | Line chart, Area chart | Show change over time |
| Part of whole | Pie chart, Donut chart, Treemap | Show composition |
| Relationship | Scatter plot, Bubble chart | Show correlation |
| Distribution | Histogram, Box plot | Show data spread |
| Hierarchical | Treemap, Sunburst | Show nested data |
| Network | Force-directed graph | Show connections |
| Geographic | Choropleth map | Show regional data |
| Multi-dimensional | Radar chart | Compare multiple variables |

---

## D3.js Patterns

### Basic Bar Chart
```javascript
const data = [30, 86, 168, 281, 303, 365];

const svg = d3.select("body").append("svg")
  .attr("width", 400)
  .attr("height", 300);

const x = d3.scaleBand()
  .domain(data.map((d, i) => i))
  .range([0, 400])
  .padding(0.1);

const y = d3.scaleLinear()
  .domain([0, d3.max(data)])
  .range([300, 0]);

svg.selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", (d, i) => x(i))
  .attr("y", d => y(d))
  .attr("width", x.bandwidth())
  .attr("height", d => 300 - y(d))
  .attr("fill", "#2563eb")
  .transition()
  .duration(800)
  .delay((d, i) => i * 100)
  .attr("fill", "#3b82f6");
```

### Interactive Line Chart
```javascript
const data = [
  {date: "2024-01", value: 30},
  {date: "2024-02", value: 86},
  {date: "2024-03", value: 168},
  {date: "2024-04", value: 281},
  {date: "2024-05", value: 303},
];

const svg = d3.select("chart").append("svg")
  .attr("width", 600)
  .attr("height", 400);

const x = d3.scalePoint()
  .domain(data.map(d => d.date))
  .range([50, 550]);

const y = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.value)])
  .range([350, 50]);

const line = d3.line()
  .x(d => x(d.date))
  .y(d => y(d.value))
  .curve(d3.curveMonotoneX);

svg.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "#2563eb")
  .attr("stroke-width", 3)
  .attr("d", line);

// Tooltip
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

svg.selectAll("circle")
  .data(data)
  .join("circle")
  .attr("cx", d => x(d.date))
  .attr("cy", d => y(d.value))
  .attr("r", 5)
  .attr("fill", "#2563eb")
  .on("mouseover", (event, d) => {
    tooltip.transition().duration(200).style("opacity", 1);
    tooltip.html(`${d.date}: ${d.value}`)
      .style("left", (event.pageX + 10) + "px")
      .style("top", (event.pageY - 28) + "px");
  })
  .on("mouseout", () => {
    tooltip.transition().duration(500).style("opacity", 0);
  });
```

### Donut Chart
```javascript
const data = [30, 86, 168, 281];
const colors = ["#2563eb", "#10b981", "#f59e0b", "#ef4444"];

const svg = d3.select("chart").append("svg")
  .attr("width", 300)
  .attr("height", 300);

const g = svg.append("g")
  .attr("transform", "translate(150,150)");

const pie = d3.pie().value(d => d);
const arc = d3.arc().innerRadius(80).outerRadius(120);

g.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => colors[i])
  .transition()
  .duration(800)
  .attrTween("d", function(d) {
    const interpolate = d3.interpolate({startAngle: 0, endAngle: 0}, d);
    return function(t) { return arc(interpolate(t)); };
  });
```

### Treemap
```javascript
const data = {
  name: "root",
  children: [
    {name: "A", value: 300},
    {name: "B", value: 200},
    {name: "C", value: 150},
    {name: "D", value: 100},
  ]
};

const width = 600, height = 400;

const treemap = d3.treemap()
  .size([width, height])
  .padding(2);

const root = d3.hierarchy(data)
  .sum(d => d.value);

treemap(root);

const svg = d3.select("chart").append("svg")
  .attr("width", width)
  .attr("height", height);

svg.selectAll("rect")
  .data(root.leaves())
  .join("rect")
  .attr("x", d => d.x0)
  .attr("y", d => d.y0)
  .attr("width", d => d.x1 - d.x0)
  .attr("height", d => d.y1 - d.y0)
  .attr("fill", "#3b82f6")
  .attr("rx", 4);
```

---

## Animation Patterns

### Transitions
```javascript
// Basic transition
selection.transition()
  .duration(800)
  .delay((d, i) => i * 100)
  .attr("fill", "#10b981");

// Easing
d3.easeElasticOut
d3.easeBounceOut
d3.easeCubicInOut
```

### Scroll-Triggered
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      animateChart();
      observer.unobserve(entry.target);
    }
  });
});
observer.observe(document.getElementById("chart"));
```

---

## Styling

```css
.chart-container {
  background: var(--bg);
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-md);
}

.axis text {
  font-family: var(--font-body);
  font-size: 12px;
  fill: var(--text-light);
}

.axis line, .axis path {
  stroke: var(--border);
}

.grid line {
  stroke: var(--border);
  stroke-opacity: 0.3;
}

.tooltip {
  position: absolute;
  background: var(--text);
  color: var(--bg);
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  pointer-events: none;
}
```

---

## Output
- Complete HTML file with embedded D3.js
- Responsive design
- Tooltips for interactivity
- Smooth animations
- Clean, accessible code
