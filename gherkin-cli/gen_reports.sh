#!/bin/bash
# Generate reports from feature files

mkdir -p reports

echo "🚀 Running Gherkin tests and generating reports..."
echo ""

# Run behave with all three formatters in one command
behave \
  --format plain --outfile reports/report.txt \
  --format json --outfile reports/report.json \
  --format behave_html_formatter:HTMLFormatter --outfile reports/report.html

echo ""
echo "✅ Reports generated:"
ls -lh reports/report.*
