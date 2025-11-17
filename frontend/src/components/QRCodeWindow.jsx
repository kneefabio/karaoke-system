import { QRCodeSVG } from 'qrcode.react';
import { Button } from "@/components/ui/button";
import { Printer, Download } from "lucide-react";

const QRCodeWindow = () => {
  // Ottieni token di sessione dall'URL
  const urlParams = new URLSearchParams(window.location.search);
  const sessionToken = urlParams.get('token');
  
  const bookingUrl = `${window.location.origin}/book?token=${encodeURIComponent(sessionToken)}`;

  const handlePrint = () => {
    window.print();
  };

  const handleDownload = () => {
    const svg = document.getElementById('qr-code-svg');
    const svgData = new XMLSerializer().serializeToString(svg);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      const pngFile = canvas.toDataURL('image/png');
      
      const downloadLink = document.createElement('a');
      downloadLink.download = 'qrcode-prenotazioni.png';
      downloadLink.href = pngFile;
      downloadLink.click();
    };
    
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 flex flex-col items-center justify-center p-8">
      <style>{`
        @media print {
          body * {
            visibility: hidden;
          }
          #qr-print-area, #qr-print-area * {
            visibility: visible;
          }
          #qr-print-area {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
          }
          .no-print {
            display: none !important;
          }
        }
      `}</style>
      
      <div id="qr-print-area" className="bg-white rounded-3xl shadow-2xl p-12 max-w-2xl w-full text-center">
        <h1 className="text-5xl font-bold text-purple-900 mb-4">
          🎤 Prenota Karaoke
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Scansiona il QR Code per prenotare la tua canzone!
        </p>
        
        <div className="flex justify-center mb-8">
          <div className="p-8 bg-white rounded-2xl shadow-lg">
            <QRCodeSVG 
              id="qr-code-svg"
              value={bookingUrl}
              size={400}
              level="H"
              includeMargin={true}
            />
          </div>
        </div>
        
        <div className="space-y-3 text-left bg-purple-50 p-6 rounded-xl">
          <p className="text-lg text-gray-700">
            📱 <strong>Passo 1:</strong> Scansiona il QR Code
          </p>
          <p className="text-lg text-gray-700">
            ✍️ <strong>Passo 2:</strong> Compila il form
          </p>
          <p className="text-lg text-gray-700">
            🎵 <strong>Passo 3:</strong> La tua canzone è in lista!
          </p>
        </div>
        
        <p className="text-sm text-gray-500 mt-8">
          {bookingUrl}
        </p>
      </div>
      
      <div className="mt-8 flex gap-4 no-print">
        <Button 
          onClick={handlePrint} 
          size="lg"
          className="bg-white text-purple-900 hover:bg-purple-100"
        >
          <Printer className="mr-2 h-5 w-5" />
          Stampa QR Code
        </Button>
        
        <Button 
          onClick={handleDownload} 
          size="lg"
          variant="outline"
          className="bg-white text-purple-900 hover:bg-purple-100"
        >
          <Download className="mr-2 h-5 w-5" />
          Scarica PNG
        </Button>
      </div>
      
      <p className="text-white mt-6 text-sm no-print">
        💡 Puoi trascinare questa finestra su un altro schermo
      </p>
    </div>
  );
};

export default QRCodeWindow;
