// Export PDF for color_analysis page
(function(){
  function isColorAnalysisPage() {
    return window.location.pathname.includes('color-analysis') || !!document.querySelector('.color-analysis-scope');
  }

  function loadScript(url) {
    return new Promise(function(resolve, reject) {
      const s = document.createElement('script');
      s.src = url;
      s.onload = () => resolve();
      s.onerror = () => reject(new Error('Failed to load ' + url));
      document.head.appendChild(s);
    });
  }

  async function ensureLibs() {
    const libs = [];
    if (typeof html2canvas === 'undefined') {
      libs.push('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js');
    }
    if (typeof window.jspdf === 'undefined' && typeof window.jsPDF === 'undefined') {
      libs.push('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
    }

    for (const url of libs) {
      await loadScript(url);
    }
  }

  async function exportColorAnalysisPDF() {
    const el = document.querySelector('.color-analysis-scope');
    if (!el) {
      alert('This export is available on the Color Analysis page only.');
      return;
    }

    await ensureLibs();

    if (typeof html2canvas === 'undefined') {
      alert('html2canvas is not available. Cannot export.');
      return;
    }

    const jsPDFConstructor = (window.jspdf && window.jspdf.jsPDF) ? window.jspdf.jsPDF : (window.jsPDF ? window.jsPDF : null);
    if (!jsPDFConstructor) {
      alert('jsPDF is not available. Cannot export.');
      return;
    }

    const originalScroll = window.scrollY;
    window.scrollTo(0,0);

    const btn = document.getElementById('export-pdf-btn');
    const prevHtml = btn ? btn.innerHTML : '';
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>'; }

    try {
      const canvas = await html2canvas(el, {scale: 2, useCORS: true, allowTaint: true});
      const imgData = canvas.toDataURL('image/png');

      const pdf = new jsPDFConstructor('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();

      const imgProps = { width: canvas.width, height: canvas.height };
      let pdfImgWidth = pageWidth;
      let pdfImgHeight = (imgProps.height * pdfImgWidth) / imgProps.width;

      if (pdfImgHeight > pageHeight) {
        pdfImgHeight = pageHeight;
        pdfImgWidth = (imgProps.width * pdfImgHeight) / imgProps.height;
      }

      const marginLeft = (pageWidth - pdfImgWidth) / 2;
      const marginTop = (pageHeight - pdfImgHeight) / 2;

      pdf.addImage(imgData, 'PNG', marginLeft, marginTop, pdfImgWidth, pdfImgHeight, undefined, 'FAST');
      pdf.save('color-analysis.pdf');

    } catch (err) {
      console.error('Export PDF failed', err);
      alert('Could not export PDF. See console for details.');
    } finally {
      if (btn) { btn.disabled = false; btn.innerHTML = prevHtml; }
      window.scrollTo(0, originalScroll);
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('export-pdf-btn');
    if (!btn) return;

    btn.addEventListener('click', function(e) {
      if (!isColorAnalysisPage()) {
        const go = confirm('Open Color Analysis page to export current analysis as PDF?');
        if (go) { window.location.href = '/color-analysis'; }
        return;
      }
      exportColorAnalysisPDF();
    });
  });
})();
