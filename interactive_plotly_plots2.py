import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Example data
hist_data = np.random.normal(loc=0, scale=1, size=1000)
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create the first histogram
hist1, edges1 = np.histogram(hist_data, bins=30)
fig1 = go.Figure()
fig1.add_trace(go.Histogram(x=hist_data, nbinsx=30, marker_color='red'))

# Create the second histogram
hist2, edges2 = np.histogram(hist_data, bins=30)
fig2 = go.Figure()
fig2.add_trace(go.Histogram(x=hist_data, nbinsx=30, marker_color='blue'))

# Create the first line plot
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=x, y=y1, mode='lines', line=dict(color='green')))

# Create the second line plot
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=x, y=y2, mode='lines', line=dict(color='purple')))

# Predefined threshold values
thresholds = [1, 2, 3, 4, 5]

# Create subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=("Histogram 1", "Histogram 2", "Line Plot 1", "Line Plot 2"))

# Add histograms to subplots
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)

# Add line plots to subplots
fig.add_trace(fig3.data[0], row=2, col=1)
fig.add_trace(fig4.data[0], row=2, col=2)

# Create vertical line traces for thresholds
line_traces = []
for threshold in thresholds:
    line_trace = go.Scatter(x=[threshold, threshold], y=[0, 1], mode='lines',
                           line=dict(color='black', dash='dash'), showlegend=False)
    line_traces.append(line_trace)

# Initialize selected thresholds with all thresholds
selected_thresholds = thresholds.copy()

# Update plot annotations on threshold selection
def update_annotations(selected_thresholds):
    updated_line_traces = []
    for line_trace in line_traces:
        if line_trace.x[0] in selected_thresholds:
            updated_line_traces.append(line_trace)
    fig.update_traces(updates={'x': [], 'y': []})  # Clear existing line traces
    fig.add_traces(updated_line_traces)  # Add updated line traces

# Initialize line traces
fig.add_traces(line_traces)

# Define JavaScript code
js_code = """
function updateThresholds() {
    var checkboxes = document.getElementsByClassName('threshold-checkbox');
    var selectedThresholds = [];
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedThresholds.push(parseFloat(checkboxes[i].value));
        }
    }
    // Call the update_annotations function in Python via the Pyodide interface
    pyodide.globals.update_annotations(selectedThresholds);
}

// Attach click event listener to checkboxes
var checkboxes = document.getElementsByClassName('threshold-checkbox');
for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener('click', updateThresholds);
}
"""

# Create checkboxes HTML
checkboxes_html = "<br>".join([
    f"<input type='checkbox' class='threshold-checkbox' value='{threshold}' checked> {threshold}"
    for threshold in thresholds
])
checkboxes_html += "<br><br>"

# Save the plot as an HTML file
fig.update_layout(annotations=[])  # Remove existing annotations
fig.write_html("threshold_plot.html", include_plotlyjs="cdn")

print("Graph saved as 'threshold_plot.html'. Open the file in your browser to view the graph and select thresholds.")
