export function downloadPDF(blob: Blob, filename: string): void {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

export function getReportFilename(type: 'horoscope' | 'matchmaking', language: string): string {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const languageSuffix = {
    en: 'English',
    ml: 'Malayalam',
    ta: 'Tamil',
  }[language] || 'English';

  return `${type}_report_${timestamp}_${languageSuffix}.pdf`;
} 