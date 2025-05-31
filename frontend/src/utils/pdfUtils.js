import jsPDF from 'jspdf';

export const generateHoroscopePDF = (result) => {
  const doc = new jsPDF();
  let y = 20;

  // Title
  doc.setFontSize(20);
  doc.text('Horoscope Report', 20, y);
  y += 10;

  // Personal Details
  doc.setFontSize(16);
  doc.text('Personal Details', 20, y);
  y += 10;
  doc.setFontSize(12);
  doc.text(`Name: ${result.name}`, 30, y);
  y += 7;
  doc.text(`Gender: ${result.gender}`, 30, y);
  y += 7;
  doc.text(`Date of Birth: ${result.date_of_birth}`, 30, y);
  y += 7;
  doc.text(`Time of Birth: ${result.time_of_birth}`, 30, y);
  y += 7;
  doc.text(`Place: ${result.place_name}`, 30, y);
  y += 10;

  // Planetary Positions
  doc.setFontSize(16);
  doc.text('Planetary Positions', 20, y);
  y += 10;
  const positions = result.planetary_positions || {};
  const planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];
  planets.forEach(planet => {
    const pos = positions[planet];
    if (pos) {
      doc.setFontSize(12);
      doc.text(`${planet}: ${pos.dms} (${pos.rasi})`, 30, y);
      y += 7;
    }
  });
  y += 10;

  // Planetary Strength Analysis (always show section)
  doc.setFontSize(16);
  doc.text('Planetary Strength Analysis', 20, y);
  y += 10;
  doc.setFontSize(12);
  if (result.planetary_strengths && Object.keys(result.planetary_strengths).length > 0) {
    Object.entries(result.planetary_strengths).forEach(([planet, strengths]) => {
      doc.text(`${planet}:`, 30, y);
      y += 7;
      Object.entries(strengths).forEach(([key, value]) => {
        doc.text(`  ${key}: ${value}`, 40, y);
        y += 7;
      });
      y += 3;
    });
    y += 10;
  } else {
    doc.text('No planetary strength data available.', 30, y);
    y += 10;
  }

  // Predictions
  doc.setFontSize(16);
  doc.text('Predictions', 20, y);
  y += 10;
  const predictions = result.predictions || {};
  Object.entries(predictions).forEach(([category, text]) => {
    doc.setFontSize(12);
    doc.text(`${category}:`, 30, y);
    y += 7;
    const lines = doc.splitTextToSize(text, 170);
    lines.forEach(line => {
      doc.text(line, 40, y);
      y += 7;
    });
    y += 3;
  });

  return doc;
};

export const downloadPDF = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};

export const getReportFilename = (type, language) => {
  const date = new Date().toISOString().split('T')[0];
  return `${type}_report_${language}_${date}.pdf`;
}; 