import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Trash2, Check, X, LogOut, Users, Music, ListChecks, Clock, Shield, Camera } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function AdminDashboard() {
  const [singers, setSingers] = useState([]);
  const [stats, setStats] = useState(null);
  const [bookingsOpen, setBookingsOpen] = useState(true);
  const [loading, setLoading] = useState(true);
  const [isSuperAdmin, setIsSuperAdmin] = useState(false);
  const [licenseInfo, setLicenseInfo] = useState(null);
  const navigate = useNavigate();

  const token = localStorage.getItem("admin_token");

  useEffect(() => {
    if (!token) {
      navigate("/admin/login");
      return;
    }
    fetchData();
    checkSuperAdmin();
    fetchLicenseInfo();
    const interval = setInterval(fetchData, 3000); // Poll every 3 seconds
    const licenseInterval = setInterval(checkLicense, 300000); // Check license every 5 minutes
    return () => {
      clearInterval(interval);
      clearInterval(licenseInterval);
    };
  }, []);

  const checkSuperAdmin = async () => {
    try {
      const response = await axios.get(`${API}/admin/my-license`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.data.unlimited && response.data.role === "super_admin") {
        setIsSuperAdmin(true);
      }
    } catch (error) {
      // Not super admin
    }
  };

  const fetchData = async () => {
    try {
      const [singersRes, statsRes, settingsRes] = await Promise.all([
        axios.get(`${API}/admin/singers`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/admin/stats`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/settings`)
      ]);

      setSingers(singersRes.data);
      setStats(statsRes.data);
      setBookingsOpen(settingsRes.data.prenotazioni_aperte);
      setLoading(false);
    } catch (error) {
      if (error.response?.status === 401) {
        localStorage.removeItem("admin_token");
        navigate("/admin/login");
      }
      console.error("Error fetching data:", error);
    }
  };

  const toggleBookings = async () => {
    try {
      await axios.put(
        `${API}/admin/settings`,
        { prenotazioni_aperte: !bookingsOpen },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setBookingsOpen(!bookingsOpen);
      toast.success(bookingsOpen ? "Prenotazioni chiuse" : "Prenotazioni aperte");
    } catch (error) {
      toast.error("Errore nell'aggiornamento");
    }
  };

  const toggleSongStatus = async (songId, currentStatus) => {
    try {
      await axios.put(
        `${API}/admin/song/${songId}`,
        { cantata: !currentStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchData();
      toast.success(!currentStatus ? "Canzone marcata come cantata" : "Canzone ripristinata");
    } catch (error) {
      toast.error("Errore nell'aggiornamento");
    }
  };

  const deleteSong = async (songId) => {
    if (!window.confirm("Sei sicuro di voler eliminare questa canzone?")) return;

    try {
      await axios.delete(`${API}/admin/song/${songId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchData();
      toast.success("Canzone eliminata");
    } catch (error) {
      toast.error("Errore nell'eliminazione");
    }
  };

  const deleteSinger = async (singerId) => {
    if (!window.confirm("Sei sicuro di voler eliminare questo cantante e tutte le sue canzoni?")) return;

    try {
      await axios.delete(`${API}/admin/singer/${singerId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchData();
      toast.success("Cantante eliminato");
    } catch (error) {
      toast.error("Errore nell'eliminazione");
    }
  };

  const logout = () => {
    localStorage.removeItem("admin_token");
    navigate("/admin/login");
  };

  const handleResetAll = async () => {
    if (!window.confirm("⚠️ ATTENZIONE! Questa azione cancellerà TUTTI i cantanti e TUTTE le canzoni. Sei sicuro?")) return;
    
    try {
      await axios.delete(`${API}/admin/reset-all`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchData();
      toast.success("Serata resettata completamente");
    } catch (error) {
      toast.error("Errore durante il reset");
    }
  };

  const handleClearSung = async () => {
    if (!window.confirm("Vuoi eliminare tutte le canzoni già cantate? I cantanti rimarranno.")) return;
    
    try {
      const response = await axios.delete(`${API}/admin/clear-sung`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchData();
      toast.success(response.data.message);
    } catch (error) {
      toast.error("Errore durante la pulizia");
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Caricamento...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6" data-testid="admin-dashboard">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold mb-2" style={{ fontFamily: 'Space Grotesk' }}>Dashboard Admin</h1>
            <p className="text-gray-600">Gestione prenotazioni karaoke</p>
          </div>
          <div className="flex gap-3">
            <Button 
              onClick={() => navigate("/admin/serate")}
              variant="outline"
              className="flex items-center gap-2 border-blue-500 text-blue-600 hover:bg-blue-50"
              data-testid="serate-btn"
            >
              <Camera className="w-4 h-4" />
              Foto Serate
            </Button>
            {isSuperAdmin && (
              <Button 
                onClick={() => navigate("/super-admin")}
                variant="outline"
                className="flex items-center gap-2 border-purple-500 text-purple-600 hover:bg-purple-50"
                data-testid="super-admin-btn"
              >
                <Shield className="w-4 h-4" />
                Super Admin
              </Button>
            )}
            <Button 
              onClick={handleClearSung}
              variant="outline"
              className="flex items-center gap-2 border-orange-500 text-orange-600 hover:bg-orange-50"
              data-testid="clear-sung-btn"
            >
              <ListChecks className="w-4 h-4" />
              Elimina Cantate
            </Button>
            <Button 
              onClick={handleResetAll}
              variant="outline"
              className="flex items-center gap-2 border-red-500 text-red-600 hover:bg-red-50"
              data-testid="reset-all-btn"
            >
              <Trash2 className="w-4 h-4" />
              Reset Serata
            </Button>
            <Button 
              onClick={logout} 
              variant="outline" 
              className="flex items-center gap-2"
              data-testid="logout-btn"
            >
              <LogOut className="w-4 h-4" />
              Esci
            </Button>
          </div>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Totale Cantanti</CardTitle>
                <Users className="w-5 h-5 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stats.totale_cantanti}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Totale Prenotazioni</CardTitle>
                <Music className="w-5 h-5 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stats.totale_prenotazioni}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Canzoni Cantate</CardTitle>
                <ListChecks className="w-5 h-5 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stats.canzoni_cantate}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">In Attesa</CardTitle>
                <Clock className="w-5 h-5 text-orange-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{stats.in_attesa}</div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Bookings Toggle */}
        <Card className="mb-8">
          <CardContent className="flex items-center justify-between p-6">
            <div>
              <h3 className="text-lg font-semibold mb-1">Stato Prenotazioni</h3>
              <p className="text-sm text-gray-600">
                {bookingsOpen ? "Le prenotazioni sono aperte" : "Le prenotazioni sono chiuse"}
              </p>
            </div>
            <Switch 
              checked={bookingsOpen} 
              onCheckedChange={toggleBookings}
              data-testid="toggle-bookings-switch"
            />
          </CardContent>
        </Card>

        {/* Singers List */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Lista Cantanti ({singers.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {singers.length === 0 ? (
              <p className="text-center text-gray-500 py-8">Nessuna prenotazione al momento</p>
            ) : (
              <div className="space-y-6">
                {singers.map((singer) => (
                  <div key={singer.id} className="border rounded-lg p-5 bg-white shadow-sm" data-testid={`singer-row-${singer.codice}`}>
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="flex items-center gap-3">
                          <h3 className="text-xl font-semibold">{singer.nome}</h3>
                          <Badge variant="outline" className="text-xs">#{singer.codice}</Badge>
                        </div>
                        <p className="text-sm text-gray-500 mt-1">{singer.canzoni.length} canzon{singer.canzoni.length === 1 ? 'e' : 'i'}</p>
                      </div>
                      <Button 
                        onClick={() => deleteSinger(singer.id)} 
                        variant="ghost" 
                        size="sm"
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        data-testid={`delete-singer-${singer.codice}`}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>

                    <div className="space-y-2">
                      {singer.canzoni.map((song) => (
                        <div 
                          key={song.id} 
                          className={`flex items-center justify-between p-3 rounded-md border ${
                            song.cantata ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
                          }`}
                          data-testid={`song-${song.id}`}
                        >
                          <div className="flex items-center gap-3 flex-1">
                            <Badge variant="secondary" className="text-xs font-mono">#{song.ordine_prenotazione}</Badge>
                            <div>
                              <p className={`font-medium ${song.cantata ? 'line-through text-gray-500' : ''}`}>
                                {song.canzone}
                              </p>
                              <p className="text-sm text-gray-500">Tonalità: {song.tonalita}</p>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Button
                              onClick={() => toggleSongStatus(song.id, song.cantata)}
                              size="sm"
                              variant={song.cantata ? "outline" : "default"}
                              className={song.cantata ? "" : "bg-green-600 hover:bg-green-700"}
                              data-testid={`toggle-song-${song.id}`}
                            >
                              {song.cantata ? <X className="w-4 h-4" /> : <Check className="w-4 h-4" />}
                            </Button>
                            <Button
                              onClick={() => deleteSong(song.id)}
                              size="sm"
                              variant="ghost"
                              className="text-red-600 hover:text-red-700 hover:bg-red-50"
                              data-testid={`delete-song-${song.id}`}
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
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