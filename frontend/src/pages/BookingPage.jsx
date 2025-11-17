import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { Music, Mic2, Hash } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function BookingPage() {
  const [searchParams] = useSearchParams();
  const [sessionToken, setSessionToken] = useState(null);
  const [adminUsername, setAdminUsername] = useState(null);
  const [tokenValid, setTokenValid] = useState(false);
  const [formData, setFormData] = useState({
    nome: "",
    email: "",
    canzone: "",
    tonalita: "",
    codice: ""
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const validateToken = async () => {
      // Prova prima con il token
      const token = searchParams.get('token');
      
      if (token) {
        try {
          // Valida il token con il backend
          const response = await axios.get(`${API}/booking-session/validate/${token}`);
          setSessionToken(token);
          setAdminUsername(response.data.admin_username);
          setTokenValid(true);
        } catch (error) {
          toast.error("Token di sessione non valido o scaduto");
          setTokenValid(false);
        }
      } else {
        // Fallback al vecchio sistema con admin username (per compatibilità)
        const admin = searchParams.get('admin');
        if (admin) {
          setAdminUsername(admin);
          setTokenValid(true);
        } else {
          toast.error("Link non valido: manca l'identificativo del host");
          setTokenValid(false);
        }
      }
    };
    
    validateToken();
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.nome || !formData.canzone || !formData.tonalita) {
      toast.error("Compila tutti i campi obbligatori");
      return;
    }

    if (!tokenValid) {
      toast.error("Sessione non valida");
      return;
    }

    setLoading(true);

    try {
      const bookingData = {
        nome: formData.nome,
        email: formData.email || null,
        canzone: formData.canzone,
        tonalita: formData.tonalita,
        codice: formData.codice || null
      };
      
      // Usa il token di sessione se disponibile, altrimenti admin_username (per compatibilità)
      if (sessionToken) {
        bookingData.session_token = sessionToken;
      } else {
        bookingData.admin_username = adminUsername;
      }
      
      const response = await axios.post(`${API}/book`, bookingData);

      if (response.data.nuovo_cantante) {
        toast.success(response.data.message, { duration: 6000 });
      } else {
        toast.success(response.data.message);
      }

      // Reset form except codice
      setFormData({
        nome: formData.nome,
        email: formData.email,
        canzone: "",
        tonalita: "",
        codice: response.data.codice
      });
    } catch (error) {
      const message = error.response?.data?.detail || "Errore durante la prenotazione";
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{ background: 'linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%)' }}>
      <Card className="w-full max-w-lg shadow-lg border-0" data-testid="booking-form-card">
        <CardHeader className="text-center space-y-2 pb-6">
          <div className="flex justify-center mb-3">
            <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-4 rounded-2xl shadow-md">
              <Mic2 className="w-10 h-10 text-white" />
            </div>
          </div>
          <CardTitle className="text-4xl font-bold" style={{ fontFamily: 'Space Grotesk' }}>Prenota Karaoke</CardTitle>
          <CardDescription className="text-base">Inserisci i tuoi dati per prenotare una canzone</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <Label htmlFor="codice" className="text-sm font-medium flex items-center gap-2">
                <Hash className="w-4 h-4" />
                Codice (opzionale)
              </Label>
              <Input
                id="codice"
                name="codice"
                value={formData.codice}
                onChange={handleChange}
                placeholder="Inserisci il tuo codice se ti sei già prenotato"
                className="h-11"
                data-testid="codice-input"
              />
              <p className="text-xs text-gray-500">Se hai già prenotato, inserisci il tuo codice per aggiungere nuove canzoni</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="nome" className="text-sm font-medium">Nome *</Label>
              <Input
                id="nome"
                name="nome"
                value={formData.nome}
                onChange={handleChange}
                placeholder="Il tuo nome"
                required
                className="h-11"
                data-testid="nome-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium">Email (opzionale)</Label>
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Per ricevere le foto della serata"
                className="h-11"
                data-testid="email-input"
              />
              <p className="text-xs text-gray-500">Riceverai le foto della serata via email</p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="canzone" className="text-sm font-medium flex items-center gap-2">
                <Music className="w-4 h-4" />
                Canzone *
              </Label>
              <Input
                id="canzone"
                name="canzone"
                value={formData.canzone}
                onChange={handleChange}
                placeholder="Titolo della canzone"
                required
                className="h-11"
                data-testid="canzone-input"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="tonalita" className="text-sm font-medium">Tonalità *</Label>
              <Input
                id="tonalita"
                name="tonalita"
                value={formData.tonalita}
                onChange={handleChange}
                placeholder="Es: Do, Re, Mi, originale, +1, -2"
                required
                className="h-11"
                data-testid="tonalita-input"
              />
            </div>

            <Button 
              type="submit" 
              className="w-full h-12 text-base font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg"
              disabled={loading}
              data-testid="submit-booking-btn"
            >
              {loading ? "Invio..." : "Invia Prenotazione"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}