import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle, Mail, Phone, MessageCircle, LogOut } from "lucide-react";

export default function NoLicensePage({ reason = "missing" }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("admin_token");
    navigate("/admin/login");
  };

  const messages = {
    missing: {
      title: "Licenza Mancante",
      icon: "🔐",
      description: "Non hai una licenza attiva associata al tuo account.",
      color: "orange"
    },
    expired: {
      title: "Licenza Scaduta",
      icon: "⏰",
      description: "La tua licenza è scaduta e non puoi più accedere al sistema.",
      color: "red"
    },
    suspended: {
      title: "Licenza Sospesa",
      icon: "⚠️",
      description: "La tua licenza è stata sospesa. Contatta l'assistenza.",
      color: "red"
    }
  };

  const currentMessage = messages[reason] || messages.missing;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-6">
      <Card className="max-w-2xl w-full shadow-2xl">
        <CardHeader className="text-center pb-4">
          <div className="flex justify-center mb-4">
            <div className={`text-6xl bg-${currentMessage.color}-100 rounded-full p-6`}>
              {currentMessage.icon}
            </div>
          </div>
          <CardTitle className="text-3xl font-bold text-gray-900">
            {currentMessage.title}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Messaggio Principale */}
          <div className="bg-gray-50 border-l-4 border-orange-500 p-4 rounded-r-lg">
            <div className="flex items-start">
              <AlertCircle className="h-6 w-6 text-orange-500 mr-3 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-gray-900 mb-2">
                  Accesso Negato
                </p>
                <p className="text-gray-700">
                  {currentMessage.description}
                </p>
                <p className="text-gray-600 mt-2">
                  Per continuare ad utilizzare il sistema karaoke, è necessaria una licenza valida e attiva.
                </p>
              </div>
            </div>
          </div>

          {/* Cosa Fare */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
              📋 Cosa Puoi Fare
            </h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Contatta il tuo amministratore di sistema (Super Admin) per richiedere l'assegnazione di una licenza</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Se sei il proprietario, acquista o rinnova la licenza tramite i contatti assistenza</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Verifica che la licenza non sia scaduta o sospesa</span>
              </li>
            </ul>
          </div>

          {/* Contatti Assistenza */}
          <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-6 rounded-lg border border-purple-200">
            <h3 className="font-bold text-purple-900 mb-4 text-lg">
              💬 Contatti Assistenza
            </h3>
            <div className="space-y-3">
              <a 
                href="mailto:support@karaokeapp.com" 
                className="flex items-center gap-3 p-3 bg-white rounded-lg hover:shadow-md transition group"
              >
                <Mail className="h-5 w-5 text-purple-600 group-hover:text-purple-700" />
                <div>
                  <div className="font-semibold text-gray-900">Email</div>
                  <div className="text-sm text-gray-600">support@karaokeapp.com</div>
                </div>
              </a>

              <a 
                href="tel:+393001234567" 
                className="flex items-center gap-3 p-3 bg-white rounded-lg hover:shadow-md transition group"
              >
                <Phone className="h-5 w-5 text-purple-600 group-hover:text-purple-700" />
                <div>
                  <div className="font-semibold text-gray-900">Telefono</div>
                  <div className="text-sm text-gray-600">+39 300 123 4567</div>
                </div>
              </a>

              <a 
                href="https://wa.me/393001234567" 
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 bg-white rounded-lg hover:shadow-md transition group"
              >
                <MessageCircle className="h-5 w-5 text-green-600 group-hover:text-green-700" />
                <div>
                  <div className="font-semibold text-gray-900">WhatsApp</div>
                  <div className="text-sm text-gray-600">+39 300 123 4567</div>
                </div>
              </a>
            </div>
          </div>

          {/* Info Licenze */}
          <div className="bg-gray-100 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-900 mb-2">
              📦 Piani Disponibili
            </h3>
            <div className="grid grid-cols-3 gap-3 text-center text-sm">
              <div className="bg-white p-3 rounded">
                <div className="font-bold text-purple-600">1 Sera</div>
                <div className="text-xs text-gray-600">€14.90</div>
              </div>
              <div className="bg-white p-3 rounded">
                <div className="font-bold text-purple-600">1 Mese</div>
                <div className="text-xs text-gray-600">€39.90</div>
              </div>
              <div className="bg-white p-3 rounded">
                <div className="font-bold text-purple-600">1 Anno</div>
                <div className="text-xs text-gray-600">€129.90</div>
              </div>
            </div>
          </div>

          {/* Pulsante Logout */}
          <div className="pt-4">
            <Button 
              onClick={handleLogout}
              variant="outline"
              className="w-full"
              size="lg"
            >
              <LogOut className="mr-2 h-5 w-5" />
              Torna al Login
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
