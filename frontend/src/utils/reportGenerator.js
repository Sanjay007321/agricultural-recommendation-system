import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export const generatePDF = async (results) => {
  const doc = new jsPDF();
  
  // Ensure autoTable is available on the doc instance
  const actualAutoTable = doc.autoTable || autoTable;
  
  if (!actualAutoTable) {
    console.error('autoTable is not defined in any form');
    throw new Error('PDF generation library not loaded correctly');
  }

  const pageWidth = doc.internal.pageSize.getWidth();
  const date = new Date().toLocaleDateString('en-IN');

  // Helper for centered text
  const centerText = (text, y, size = 16, style = 'bold') => {
    doc.setFontSize(size);
    doc.setFont('helvetica', style);
    const textWidth = doc.getTextWidth(text);
    doc.text(text, (pageWidth - textWidth) / 2, y);
  };

  // 1. Header & Title
  doc.setFillColor(34, 197, 94); // primary-500 equivalent
  doc.rect(0, 0, pageWidth, 40, 'F');
  
  doc.setTextColor(255, 255, 255);
  centerText('CROP ANALYSIS & PROFIT REPORT', 20, 22, 'bold');
  centerText(`Generated on: ${date}`, 32, 12, 'normal');
  
  doc.setTextColor(0, 0, 0);

  // 2. Overview Section
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('1. CROP RECOMMENDATION', 15, 55);
  
  actualAutoTable(doc, {
    startY: 60,
    head: [['Field', 'Details']],
    body: [
      ['Recommended Crop', results.crop_recommendation.recommended_crop],
      ['Variety', results.crop_recommendation.recommended_variety || 'Standard'],
      ['Confidence Score', `${(results.crop_recommendation.confidence * 100).toFixed(1)}%`],
      ['Land Area', `${results.land_area_acres || 'N/A'} Acres`],
      ['Soil Type', results.soil_type || 'N/A']
    ],
    theme: 'striped',
    headStyles: { fillStyle: [34, 197, 94] }
  });

  // 3. Yield & Price Section
  const yieldY = doc.lastAutoTable.finalY + 15;
  doc.text('2. YIELD & MARKET ANALYSIS', 15, yieldY);
  
  actualAutoTable(doc, {
    startY: yieldY + 5,
    head: [['Metric', 'Value']],
    body: [
      ['Expected Yield (per Acre)', `${results.yield_prediction.expected_yield_per_acre} Quintals`],
      ['Total Expected Yield', `${results.yield_prediction.total_yield_quintal} Quintals`],
      ['Current Market Price', `Rs. ${results.price_prediction.current_price_per_quintal}/Quintal`],
      ['Predicted Harvest Price', `Rs. ${results.price_prediction.predicted_price_at_harvest}/Quintal`],
      ['Price Trend', results.price_prediction.price_trend]
    ],
    theme: 'grid',
    headStyles: { fillStyle: [59, 130, 246] }
  });

  // 4. Logistics & Storage
  const logisticsY = doc.lastAutoTable.finalY + 15;
  doc.text('3. LOGISTICS & STORAGE GUIDANCE', 15, logisticsY);

  actualAutoTable(doc, {
    startY: logisticsY + 5,
    head: [['Transport Mode', 'Est. Cost', 'Nearest Mandi']],
    body: [
      [
        results.logistics_recommendation?.transport_mode || 'Local',
        `Rs. ${results.logistics_recommendation?.estimated_cost?.toLocaleString('en-IN') || '0'}`,
        results.logistics_recommendation?.nearest_mandi || 'N/A'
      ]
    ],
    theme: 'plain',
    headStyles: { fillStyle: [249, 115, 22] }
  });

  // 5. Profit Analysis (New Page if needed)
  doc.addPage();
  doc.setFillColor(34, 197, 94);
  doc.rect(0, 0, pageWidth, 20, 'F');
  centerText('PROFIT & ROI ANALYSIS', 13, 16, 'bold');
  doc.setTextColor(0, 0, 0);

  const profitData = [
    ['Total Investment', `Rs. ${results.profit_analysis.costs.total_cost.toLocaleString('en-IN')}`],
    ['Net Profit', `Rs. ${results.profit_analysis.net_profit.toLocaleString('en-IN')}`],
    ['Profit per Acre', `Rs. ${results.profit_analysis.profit_per_acre.toLocaleString('en-IN')}`],
    ['Return on Investment (ROI)', `${results.profit_analysis.roi_percentage}%`]
  ];

  actualAutoTable(doc, {
    startY: 30,
    head: [['Profit Metric', 'Amount']],
    body: profitData,
    theme: 'grid',
    headStyles: { fillStyle: [34, 197, 94] },
    columnStyles: { 1: { fontStyle: 'bold', textColor: [22, 163, 74] } }
  });

  // Cost Breakdown
  const costsY = doc.lastAutoTable.finalY + 10;
  doc.setFontSize(14);
  doc.text('Cost Breakdown:', 15, costsY);
  
  const costBreakdown = Object.entries(results.profit_analysis.costs)
    .filter(([key]) => key !== 'total_cost')
    .map(([key, value]) => [key.replace('_', ' ').toUpperCase(), `Rs. ${value.toLocaleString('en-IN')}`]);

  actualAutoTable(doc, {
    startY: costsY + 5,
    head: [['Expense Category', 'Cost']],
    body: costBreakdown,
    theme: 'striped'
  });

  // 6. Footer
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(10);
    doc.setTextColor(150);
    doc.text(`Page ${i} of ${pageCount}`, pageWidth - 30, doc.internal.pageSize.getHeight() - 10);
    doc.text('Agricultural Smart Management System', 15, doc.internal.pageSize.getHeight() - 10);
  }

  // Save the PDF
  try {
    const filenameDate = date.replace(/[\/\\]/g, '-');
    // Aggressively sanitize crop name: remove any non-alphanumeric characters except underscore and dash
    const rawCropName = results.crop_recommendation.recommended_crop || 'Crop';
    const cropName = rawCropName.replace(/[^a-z0-9]/gi, '_').replace(/_+/g, '_');
    const finalFilename = `Analysis_Report_${cropName}_${filenameDate}.pdf`;
    
    console.log(`Saving PDF as: ${finalFilename}`);
    doc.save(finalFilename);
    return true; // Indicate success
  } catch (err) {
    console.error('Save failed:', err);
    doc.save('Analysis_Report.pdf');
    return false; // Indicate partial success/fallback
  }
};

