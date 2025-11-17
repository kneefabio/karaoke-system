import { useState, useEffect, useRef } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { Camera, Check, X } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function CameraApp() {
  const [searchParams] = useSearchParams();
  const [token, setToken] = useState(null);
  const [serataInfo, setSerataInfo] = useState(null);
  const [stream, setStream] = useState(null);
  const [photo, setPhoto] = useState(null);
  const [uploading, setUploading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const urlToken = searchParams.get('token');
    if (urlToken) {
      setToken(urlToken);
      validateToken(urlToken);
      startCamera();
    } else {
      toast.error("Token mancante nell'URL");
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const validateToken = async (tkn) => {
    try {
      const response = await axios.get(`${API}/serata-token/validate/${tkn}`);
      setSerataInfo(response.data);
      toast.success("Camera pronta! 📸");
    } catch (error) {
      toast.error("Token non valido o serata terminata");
    }
  };

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }, // Usa camera posteriore
        audio: false,
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      toast.error("Impossibile accedere alla fotocamera");
    }
  };

  const takePhoto = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    console.log('📸 Taking photo...', { video, canvas });

    if (!video) {
      toast.error("Video non disponibile");
      console.error('Video ref is null');
      return;
    }

    if (!canvas) {
      toast.error("Canvas non disponibile");
      console.error('Canvas ref is null');
      return;
    }

    if (video.videoWidth === 0 || video.videoHeight === 0) {
      toast.error("Video non ancora caricato, riprova");
      console.error('Video dimensions are 0', { width: video.videoWidth, height: video.videoHeight });
      return;
    }

    console.log('Setting canvas dimensions:', { width: video.videoWidth, height: video.videoHeight });
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    canvas.toBlob((blob) => {
      console.log('✅ Photo blob created:', blob);
      setPhoto(blob);
      toast.success("Foto scattata! 📸");
    }, "image/jpeg");
  };

  const uploadPhoto = async () => {
    if (!photo || !token) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", photo, `foto_${Date.now()}.jpg`);

      await axios.post(
        `${API}/serata-token/upload?token=${token}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      toast.success("Foto caricata! ✨");
      setPhoto(null);
    } catch (error) {
      toast.error("Errore nel caricamento");
    } finally {
      setUploading(false);
    }
  };

  const cancelPhoto = () => {
    setPhoto(null);
  };

  if (!serataInfo) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-white">
        <div className="text-center">
          <p className="text-xl mb-2">📸 Camera App</p>
          <p className="text-sm text-gray-400">Validazione token in corso...</p>
          {token && <p className="text-xs text-gray-500 mt-2">Token: {token.substring(0, 8)}...</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Header */}
      <div className="p-4 bg-gray-900">
        <h1 className="text-xl font-bold text-center">📸 Serata Foto</h1>
        <p className="text-sm text-gray-400 text-center">Admin: {serataInfo.admin_username}</p>
      </div>

      {/* Hidden canvas for photo capture */}
      <canvas ref={canvasRef} style={{ display: 'none' }}></canvas>

      {/* Camera View */}
      <div className="flex-1 flex flex-col items-center justify-center p-4">
        {!photo ? (
          <div className="relative w-full max-w-2xl">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              className="w-full rounded-lg shadow-2xl"
            />
            <Button
              onClick={takePhoto}
              className="absolute bottom-4 left-1/2 transform -translate-x-1/2 w-20 h-20 rounded-full bg-white hover:bg-gray-200"
              data-testid="take-photo-btn"
            >
              <Camera className="w-8 h-8 text-black" />
            </Button>
          </div>
        ) : (
          <div className="w-full max-w-2xl">
            <Card className="bg-gray-900 border-gray-700">
              <CardHeader>
                <CardTitle className="text-white">Anteprima Foto</CardTitle>
              </CardHeader>
              <CardContent>
                <img
                  src={photo ? URL.createObjectURL(photo) : ''}
                  alt="Preview"
                  className="w-full rounded-lg mb-4"
                />
                <div className="flex gap-3">
                  <Button
                    onClick={uploadPhoto}
                    disabled={uploading}
                    className="flex-1 bg-green-600 hover:bg-green-700"
                    data-testid="upload-photo-btn"
                  >
                    <Check className="w-5 h-5 mr-2" />
                    {uploading ? "Caricamento..." : "Carica Foto"}
                  </Button>
                  <Button
                    onClick={cancelPhoto}
                    variant="outline"
                    className="flex-1 border-red-600 text-red-600 hover:bg-red-50"
                    data-testid="cancel-photo-btn"
                  >
                    <X className="w-5 h-5 mr-2" />
                    Scarta
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="p-4 bg-gray-900 text-center text-sm text-gray-400">
        <p>Scatta foto e caricale istantaneamente!</p>
        <p>Le foto appariranno sullo schermo in tempo reale.</p>
      </div>
    </div>
  );
}
