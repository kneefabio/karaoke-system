import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Key, Trash2, Plus, RefreshCw, Calendar } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function SuperAdminPanel() {
  const [licenses, setLicenses] = useState([]);
  const [admins, setAdmins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newLicense, setNewLicense] = useState({ email: "", plan: "monthly" });
  const [newAdmin, setNewAdmin] = useState({ username: "", password: "", role: "admin" });
  const [showAdminForm, setShowAdminForm] = useState(false);
  const navigate = useNavigate();

  const token = localStorage.getItem("admin_token");

  useEffect(() => {
    if (!token) {
      navigate("/admin/login");
      return;
    }
    fetchLicenses();
    fetchAdmins();
  }, []);

  const fetchLicenses = async () => {
    try {
      const response = await axios.get(`${API}/super-admin/licenses`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLicenses(response.data);
      setLoading(false);
    } catch (error) {
      if (error.response?.status === 403) {
        toast.error("Accesso negato - Solo Super Admin");
        navigate("/admin/dashboard");
      } else if (error.response?.status === 401) {
        navigate("/admin/login");
      }
    }
  };

  const fetchAdmins = async () => {
    try {
      const response = await axios.get(`${API}/super-admin/admins`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAdmins(response.data);
    } catch (error) {
      console.error("Error fetching admins:", error);
    }
  };

  const createAdmin = async () => {
    if (!newAdmin.username || !newAdmin.password) {
      toast.error("Inserisci username e password");
      return;
    }

    if (newAdmin.password.length < 6) {
      toast.error("La password deve essere almeno 6 caratteri");
      return;
    }

    try {
      const response = await axios.post(
        `${API}/super-admin/create-admin`,
        newAdmin,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast.success(response.data.message);
      setNewAdmin({ username: "", password: "", role: "admin" });
      setShowAdminForm(false);
      fetchAdmins();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Errore nella creazione dell'admin");
    }
  };

  const assignLicense = async (adminUsername, licenseKey) => {
    try {
      const response = await axios.post(
        `${API}/super-admin/assign-license`,
        { admin_username: adminUsername, license_key: licenseKey },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast.success(response.data.message);
      fetchAdmins();
      fetchLicenses();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Errore nell'assegnazione");
    }
  };

  const unassignLicense = async (adminUsername) => {
    if (!window.confirm(`Rimuovere licenza da ${adminUsername}?`)) return;

    try {
      const response = await axios.delete(
        `${API}/super-admin/unassign-license/${adminUsername}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast.success(response.data.message);
      fetchAdmins();
      fetchLicenses();
    } catch (error) {
      toast.error(error.response?.data?.detail || "Errore nella rimozione");
    }
  };

  const createLicense = async () => {
    if (!newLicense.email) {
      toast.error("Inserisci un'email");
      return;
    }

    try {
      const response = await axios.post(
        `${API}/super-admin/license/create`,
        newLicense,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast.success(`Licenza creata: ${response.data.license_key}`);
      setNewLicense({ email: "", plan: "monthly" });
      fetchLicenses();
    } catch (error) {
      toast.error("Errore nella creazione della licenza");
    }
  };

  const toggleStatus = async (licenseKey, currentStatus) => {
    const newStatus = currentStatus === "active" ? "suspended" : "active";

    try {
      await axios.put(
        `${API}/super-admin/license/${licenseKey}/status?status=${newStatus}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success(`Licenza ${newStatus === "active" ? "attivata" : "sospesa"}`);
      fetchLicenses();
    } catch (error) {
      toast.error("Errore nell'aggiornamento dello stato");
    }
  };

  const deleteLicense = async (licenseKey) => {
    if (!window.confirm("Sei sicuro di voler eliminare questa licenza?")) return;

    try {
      await axios.delete(`${API}/super-admin/license/${licenseKey}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      toast.success("Licenza eliminata");
      fetchLicenses();
    } catch (error) {
      toast.error("Errore nell'eliminazione");
    }
  };

  const extendLicense = async (licenseKey) => {
    const days = prompt("Estendi di quanti giorni?", "30");
    if (!days) return;

    try {
      await axios.put(
        `${API}/super-admin/license/${licenseKey}/extend?days=${days}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success(`Licenza estesa di ${days} giorni`);
      fetchLicenses();
    } catch (error) {
      toast.error("Errore nell'estensione");
    }
  };

  const getPlanLabel = (plan) => {
    const labels = {
      daily: "1 Sera (€14.90)",
      monthly: "1 Mese (€39.90)",
      yearly: "1 Anno (€129.90)"
    };
    return labels[plan] || plan;
  };

  const getStatusColor = (status, isExpired) => {
    if (isExpired) return "destructive";
    if (status === "active") return "default";
    if (status === "suspended") return "secondary";
    return "outline";
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Caricamento...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6" data-testid="super-admin-panel">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2" style={{ fontFamily: 'Space Grotesk' }}>
              Super Admin Panel
            </h1>
            <p className="text-gray-600">Gestione Admin e Licenze Sistema Karaoke</p>
          </div>
          <Button onClick={() => navigate("/admin/dashboard")} variant="outline">
            ← Torna alla Dashboard
          </Button>
        </div>

        {/* Gestione Admin */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="flex items-center gap-2">
                👤 Gestione Admin
              </CardTitle>
              <Button 
                onClick={() => setShowAdminForm(!showAdminForm)}
                size="sm"
                variant={showAdminForm ? "secondary" : "default"}
              >
                {showAdminForm ? "Chiudi Form" : "+ Crea Admin"}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {showAdminForm && (
              <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold mb-4">Crea Nuovo Admin</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="admin-username">Username</Label>
                    <Input
                      id="admin-username"
                      placeholder="username"
                      value={newAdmin.username}
                      onChange={(e) => setNewAdmin({ ...newAdmin, username: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="admin-password">Password</Label>
                    <Input
                      id="admin-password"
                      type="password"
                      placeholder="Min 6 caratteri"
                      value={newAdmin.password}
                      onChange={(e) => setNewAdmin({ ...newAdmin, password: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="admin-role">Ruolo</Label>
                    <Select
                      value={newAdmin.role}
                      onValueChange={(value) => setNewAdmin({ ...newAdmin, role: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="admin">Admin (Host)</SelectItem>
                        <SelectItem value="super_admin">Super Admin</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <Button onClick={createAdmin} className="mt-4">
                  Crea Admin
                </Button>
              </div>
            )}

            {/* Lista Admin */}
            <div className="space-y-3">
              <h3 className="font-semibold text-sm text-gray-600">Admin Esistenti ({admins.length})</h3>
              {admins.map((admin) => (
                <div 
                  key={admin.username} 
                  className="flex justify-between items-center p-4 bg-white border rounded-lg hover:shadow-md transition"
                >
                  <div className="flex-1">
                    <div className="font-semibold">{admin.username}</div>
                    <div className="text-sm text-gray-600">
                      Role: <Badge variant="outline">{admin.role}</Badge>
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {admin.license_key ? (
                        <>
                          🔑 Licenza: {admin.license_key.substring(0, 15)}... - {admin.license_info}
                        </>
                      ) : (
                        "⚠️ Nessuna licenza"
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    {admin.role === "super_admin" ? (
                      <Badge className="bg-purple-600">Super Admin</Badge>
                    ) : (
                      <>
                        {admin.license_key ? (
                          <Button 
                            size="sm" 
                            variant="destructive"
                            onClick={() => unassignLicense(admin.username)}
                          >
                            Rimuovi Licenza
                          </Button>
                        ) : (
                          <Select onValueChange={(licenseKey) => assignLicense(admin.username, licenseKey)}>
                            <SelectTrigger className="w-[200px]">
                              <SelectValue placeholder="Assegna Licenza" />
                            </SelectTrigger>
                            <SelectContent>
                              {licenses
                                .filter(l => !l.assigned_to || l.assigned_to === admin.username)
                                .map(license => (
                                  <SelectItem key={license.license_key} value={license.license_key}>
                                    {license.plan} - {license.license_key.substring(0, 10)}...
                                  </SelectItem>
                                ))}
                            </SelectContent>
                          </Select>
                        )}
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Crea Nuova Licenza */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Plus className="w-5 h-5" />
              Crea Nuova Licenza
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <Label htmlFor="email">Email Cliente</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="cliente@email.com"
                  value={newLicense.email}
                  onChange={(e) => setNewLicense({ ...newLicense, email: e.target.value })}
                  data-testid="new-license-email"
                />
              </div>
              <div>
                <Label htmlFor="plan">Piano</Label>
                <Select
                  value={newLicense.plan}
                  onValueChange={(value) => setNewLicense({ ...newLicense, plan: value })}
                >
                  <SelectTrigger data-testid="new-license-plan">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="daily">1 Sera (€14.90)</SelectItem>
                    <SelectItem value="monthly">1 Mese (€39.90)</SelectItem>
                    <SelectItem value="yearly">1 Anno (€129.90)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-end">
                <Button onClick={createLicense} className="w-full" data-testid="create-license-btn">
                  <Key className="w-4 h-4 mr-2" />
                  Genera Licenza
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Statistiche */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-gray-600">Totale Licenze</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{licenses.length}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-gray-600">Attive</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">
                {licenses.filter(l => l.status === "active" && !l.is_expired).length}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-gray-600">Scadute</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-600">
                {licenses.filter(l => l.is_expired).length}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-gray-600">Sospese</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">
                {licenses.filter(l => l.status === "suspended").length}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Lista Licenze */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Tutte le Licenze ({licenses.length})</CardTitle>
            <Button onClick={fetchLicenses} variant="outline" size="sm">
              <RefreshCw className="w-4 h-4" />
            </Button>
          </CardHeader>
          <CardContent>
            {licenses.length === 0 ? (
              <p className="text-center text-gray-500 py-8">Nessuna licenza creata</p>
            ) : (
              <div className="space-y-3">
                {licenses.map((license) => (
                  <div
                    key={license.license_key}
                    className="border rounded-lg p-4 bg-white hover:bg-gray-50 transition"
                    data-testid={`license-${license.license_key}`}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <code className="text-sm font-mono bg-gray-100 px-3 py-1 rounded">
                            {license.license_key}
                          </code>
                          <Badge variant={getStatusColor(license.status, license.is_expired)}>
                            {license.is_expired ? "SCADUTA" : license.status.toUpperCase()}
                          </Badge>
                          <Badge variant="outline">{getPlanLabel(license.plan)}</Badge>
                        </div>
                        <div className="text-sm text-gray-600 space-y-1">
                          <p>📧 {license.email}</p>
                          <p>📅 Scadenza: {new Date(license.expires_at).toLocaleDateString("it-IT")}</p>
                          <p className={license.days_remaining < 7 ? "text-red-600 font-semibold" : ""}>
                            ⏰ Giorni rimanenti: {license.days_remaining}
                          </p>
                          {license.last_check && (
                            <p className="text-xs">
                              Ultimo check: {new Date(license.last_check).toLocaleString("it-IT")}
                            </p>
                          )}
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button
                          onClick={() => toggleStatus(license.license_key, license.status)}
                          size="sm"
                          variant={license.status === "active" ? "outline" : "default"}
                          data-testid={`toggle-status-${license.license_key}`}
                        >
                          {license.status === "active" ? "Sospendi" : "Attiva"}
                        </Button>
                        <Button
                          onClick={() => extendLicense(license.license_key)}
                          size="sm"
                          variant="outline"
                          data-testid={`extend-${license.license_key}`}
                        >
                          <Calendar className="w-4 h-4" />
                        </Button>
                        <Button
                          onClick={() => deleteLicense(license.license_key)}
                          size="sm"
                          variant="ghost"
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                          data-testid={`delete-${license.license_key}`}
                        >
                          <Trash2 className="w-4 h-4" />
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
