import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Mail, ArrowLeft, Save, AlertCircle } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function EmailConfig() {
  const [config, setConfig] = useState({
    smtp_server: "smtp.gmail.com",
    smtp_port: 587,
    sender_email: "",
    sender_password: ""
  });
  const [loading, setLoading] = useState(false);
  const [hasExisting, setHasExisting] = useState(false);
  const navigate = useNavigate();

  const token = localStorage.getItem("admin_token");

  useEffect(() => {
    if (!token) {
      navigate("/admin/login");
      return;
    }
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await axios.get(`${API}/admin/email-config`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.success !== false) {
        setConfig({
          ...response.data,
          sender_password: "" // Non mostriamo la password
        });
        setHasExisting(true);
      }
    } catch (error) {
      // Nessuna configurazione esistente
    }
  };

  const saveConfig = async () => {
    if (!config.sender_email || !config.sender_password) {
      toast.error("Compila tutti i campi obbligatori");
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/admin/email-config`, config, {
        headers: { Authorization: `Bearer ${token}` }
      });

      toast.success("Configurazione email salvata!");
      navigate("/admin/serate");
    } catch (error) {
      toast.error("Errore nel salvataggio");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-8">
      <div className="max-w-2xl mx-auto">
        <Button
          onClick={() => navigate("/admin/serate")}
          variant="outline"
          className="mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Torna a Gestione Serate
        </Button>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Mail className="w-6 h-6" />
              Configurazione Email SMTP
            </CardTitle>
            <CardDescription>
              Configura le tue credenziali email per inviare le foto ai cantanti
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex gap-2">
                  <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                  <div className="text-sm text-blue-900">
                    <p className="font-semibold mb-2">💡 Configurazione Gmail:</p>
                    <ul className="space-y-1 list-disc list-inside">
                      <li>Usa il tuo indirizzo Gmail completo</li>
                      <li>Per la password, devi creare una <strong>"Password per le app"</strong></li>
                      <li>Vai su: Account Google → Sicurezza → Verifica in due passaggi → Password per le app</li>
                      <li>Server SMTP: smtp.gmail.com | Porta: 587</li>
                    </ul>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="smtp_server">Server SMTP</Label>
                  <Input
                    id="smtp_server"
                    value={config.smtp_server}
                    onChange={(e) => setConfig({ ...config, smtp_server: e.target.value })}
                    placeholder="smtp.gmail.com"
                  />
                </div>
                <div>
                  <Label htmlFor="smtp_port">Porta</Label>
                  <Input
                    id="smtp_port"
                    type="number"
                    value={config.smtp_port}
                    onChange={(e) => setConfig({ ...config, smtp_port: parseInt(e.target.value) })}
                    placeholder="587"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="sender_email">Email Mittente *</Label>
                <Input
                  id="sender_email"
                  type="email"
                  value={config.sender_email}
                  onChange={(e) => setConfig({ ...config, sender_email: e.target.value })}
                  placeholder="tuo-email@gmail.com"
                />
              </div>

              <div>
                <Label htmlFor="sender_password">Password / App Password *</Label>
                <Input
                  id="sender_password"
                  type="password"
                  value={config.sender_password}
                  onChange={(e) => setConfig({ ...config, sender_password: e.target.value })}
                  placeholder={hasExisting ? "Lascia vuoto per non modificare" : "Password o App Password"}
                />
                <p className="text-xs text-gray-500 mt-1">
                  {hasExisting ? "Lascia vuoto se non vuoi modificare la password esistente" : "Per Gmail usa una Password per le app"}
                </p>
              </div>

              <Button
                onClick={saveConfig}
                disabled={loading}
                className="w-full"
                size="lg"
              >
                <Save className="w-4 h-4 mr-2" />
                {loading ? "Salvataggio..." : "Salva Configurazione"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
