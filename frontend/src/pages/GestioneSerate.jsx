import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Camera, Mail, Plus, X, QrCode, ArrowLeft } from "lucide-react";
import QRCodeLib from "qrcode";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function GestioneSerate() {
  const [serate, setSerate] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newSerata, setNewSerata] = useState({ nome: "", display_time: 5 });
  const [qrCode, setQrCode] = useState(null);
  const [selectedSerata, setSelectedSerata] = useState(null);
  // ❌ RIMUOVI emailConfig e showEmailForm - non servono più!
  const navigate = useNavigate();

  const token = localStorage.getItem("admin_token");

  useEffect(() => {
    if (!token) {
      navigate("/admin/login");
      return;
    }
    fetchSerate();
  }, []);

  const fetchSerate = async () => {
    try {
      const response = await axios.get(`${API}/admin/serate`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSerate(response.data);
      setLoading(false);
    } catch (error) {
      toast.error("Errore nel caricamento serate");
    }
  };

  const createSerata = async () => {
    if (!newSerata.nome) {
      toast.error("Inserisci il nome della serata");
      return;
    }

    try {
      const response = await axios.post(
        `${API}/admin/serata/create`,
        newSerata,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast.success("Serata creata!");

      // Genera token per camera app
      const tokenResponse = await axios.post(
        `${API}/admin/serata/${response.data.serata_id}/generate-token`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Genera QR code con token
      const cameraUrl = `${window.location.origin}/camera?token=${tokenResponse.data.token}`;
      const qr = await QRCodeLib.toDataURL(cameraUrl);
      setQrCode(qr);
      setSelectedSerata({
        id: response.data.serata_id,
        token: tokenResponse.data.token
      });

      setNewSerata({ nome: "", display_time: 5 });
      fetchSerate();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Errore nella creazione");
    }
  };

  const closeSerata = async (serataId) => {
    if (!window.confirm("Chiudere la serata? Non sarà più possibile caricare foto."))
      return;

    try {
      await axios.put(
        `${API}/admin/serata/${serataId}/close`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success("Serata chiusa");
      fetchSerate();
    } catch (error) {
      toast.error("Errore nella chiusura");
    }
  };

  // ✅ NUOVA FUNZIONE CORRETTA - Controlla configurazione email prima di inviare
  const sendEmails = async (serataId) => {
    try {
      // Prima controlla se esiste una configurazione email
      const configCheck = await axios.get(`${API}/admin/email-config`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (configCheck.data.success === false || !configCheck.data.sender_email) {
        toast.error("⚠️ Configura prima le credenziali email!");
        navigate("/admin/email-config");
        return;
      }

      // Se la config esiste, invia le email
      toast.info("📧 Invio email in corso...");
      
      const response = await axios.post(
        `${API}/admin/serata/${serataId}/send-emails`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (response.data.errors && response.data.errors.length > 0) {
        toast.warning(
          `Inviate ${response.data.sent}/${response.data.total} email. Alcuni errori: ${response.data.errors.join(', ')}`
        );
      } else {
        toast.success(`✅ ${response.data.sent} email inviate con successo!`);
      }
    } catch (error) {
      if (error.response?.status === 400 && error.response?.data?.detail?.includes("Configurazione email")) {
        toast.error("⚠️ Configura prima le tue credenziali SMTP!");
        navigate("/admin/email-config");
      } else {
        toast.error(error.response?.data?.detail || "Errore nell'invio email");
      }
    }
  };

  const downloadQR = () => {
    if (!qrCode) return;
    const link = document.createElement("a");
    link.download = `qr_camera_serata.png`;
    link.href = qrCode;
    link.click();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Caricamento...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6" data-testid="gestione-serate">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1
              className="text-4xl font-bold mb-2"
              style={{ fontFamily: "Space Grotesk" }}
            >
              Gestione Serate Foto
            </h1>
            <p className="text-gray-600">Crea serate e gestisci le foto</p>
          </div>
          <div className="flex gap-2">
            <Button
              onClick={() => navigate("/admin/email-config")}
              variant="outline"
              className="border-purple-500 text-purple-600 hover:bg-purple-50"
            >
              <Mail className="w-4 h-4 mr-2" />
              Config Email
            </Button>
            <Button
              onClick={() => navigate("/admin/dashboard")}
              variant="outline"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Dashboard
            </Button>
          </div>
        </div>

        {/* Crea Nuova Serata */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Plus className="w-5 h-5" />
              Crea Nuova Serata
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="nome">Nome Serata</Label>
                <Input
                  id="nome"
                  placeholder="Es: Karaoke Estate"
                  value={newSerata.nome}
                  onChange={(e) =>
                    setNewSerata({ ...newSerata, nome: e.target.value })
                  }
                  data-testid="serata-nome"
                />
              </div>
              <div>
                <Label htmlFor="display_time">Tempo Display (secondi)</Label>
                <Input
                  id="display_time"
                  type="number"
                  min="1"
                  max="30"
                  value={newSerata.display_time}
                  onChange={(e) =>
                    setNewSerata({
                      ...newSerata,
                      display_time: parseInt(e.target.value),
                    })
                  }
                  data-testid="display-time"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Secondi per mostrare ogni foto nell'overlay
                </p>
              </div>
              <div className="flex items-end">
                <Button
                  onClick={createSerata}
                  className="w-full"
                  data-testid="create-serata-btn"
                >
                  <Camera className="w-4 h-4 mr-2" />
                  Crea Serata
                </Button>
              </div>
            </div>

            {/* QR Code e Info Serata */}
            {qrCode && selectedSerata && (
              <div className="mt-6 space-y-4">
                {/* Serata ID evidenziato */}
                <div className="p-4 bg-green-50 border-2 border-green-400 rounded-lg">
                  <h3 className="font-bold text-green-900 mb-2 flex items-center gap-2">
                    🎯 ID Serata per Overlay Electron
                  </h3>
                  <div className="bg-white p-3 rounded border-2 border-green-300">
                    <code className="text-lg font-mono font-bold text-green-700">
                      {selectedSerata.id}
                    </code>
                  </div>
                  <p className="text-sm text-green-700 mt-2">
                    👆 Copia questo ID e inseriscilo nell'overlay Electron per vedere le foto in tempo reale!
                  </p>
                </div>

                {/* QR Code Camera */}
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h3 className="font-semibold mb-3 text-blue-900">
                    📱 QR Code Camera App
                  </h3>
                  <div className="flex items-start gap-4">
                    <img
                      src={qrCode}
                      alt="QR Code"
                      className="w-48 h-48 border-4 border-white shadow-lg"
                    />
                    <div className="flex-1">
                      <p className="text-sm text-gray-700 mb-3">
                        <strong>Istruzioni:</strong>
                      </p>
                      <ol className="text-sm text-gray-600 space-y-2 list-decimal list-inside">
                        <li>Scansiona questo QR con il tuo smartphone</li>
                        <li>Si aprirà la camera app</li>
                        <li>Scatta foto durante la serata</li>
                        <li>Le foto vengono salvate automaticamente sul PC</li>
                        <li>Appaiono sull'overlay in tempo reale</li>
                      </ol>
                      <div className="mt-4 space-x-2">
                        <Button onClick={downloadQR} size="sm">
                          <QrCode className="w-4 h-4 mr-2" />
                          Scarica QR
                        </Button>
                        <Button
                          onClick={() => {
                            setQrCode(null);
                            setSelectedSerata(null);
                          }}
                          variant="outline"
                          size="sm"
                        >
                          <X className="w-4 h-4 mr-2" />
                          Chiudi
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* ❌ RIMOSSO: Card Configurazione Email - ora si fa solo da /admin/email-config */}

        {/* Lista Serate */}
        <Card>
          <CardHeader>
            <CardTitle>Serate ({serate.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {serate.length === 0 ? (
              <p className="text-center text-gray-500 py-8">
                Nessuna serata creata
              </p>
            ) : (
              <div className="space-y-3">
                {serate.map((serata) => (
                  <div
                    key={serata.id}
                    className="border rounded-lg p-4 bg-white hover:bg-gray-50 transition"
                    data-testid={`serata-${serata.id}`}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-semibold">
                            {serata.nome}
                          </h3>
                          <Badge
                            variant={serata.active ? "default" : "secondary"}
                          >
                            {serata.active ? "ATTIVA" : "CHIUSA"}
                          </Badge>
                        </div>
                        <div className="text-sm text-gray-600 space-y-1">
                          <p>📅 Data: {serata.data}</p>
                          <p>
                            📸 Foto: {serata.foto_count || 0}
                          </p>
                          <p>⏱️ Display: {serata.display_time}s per foto</p>
                          <p className="text-xs text-gray-400">
                            📁 {serata.folder_path}
                          </p>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        {serata.active && (
                          <>
                            <Button
                              onClick={() => {
                                const cameraUrl = `${BACKEND_URL}/camera/${serata.id}`;
                                QRCodeLib.toDataURL(cameraUrl).then((qr) => {
                                  setQrCode(qr);
                                  setSelectedSerata(serata.id);
                                });
                              }}
                              size="sm"
                              variant="outline"
                            >
                              <QrCode className="w-4 h-4" />
                            </Button>
                            <Button
                              onClick={() => closeSerata(serata.id)}
                              size="sm"
                              variant="outline"
                            >
                              Chiudi
                            </Button>
                          </>
                        )}
                        {/* ✅ Pulsante Invia Email con controllo configurazione */}
                        <Button
                          onClick={() => sendEmails(serata.id)}
                          size="sm"
                          className="bg-purple-600 hover:bg-purple-700"
                          disabled={serata.foto_count === 0}
                        >
                          <Mail className="w-4 h-4 mr-2" />
                          Invia Foto
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
