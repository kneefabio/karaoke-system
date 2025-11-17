import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import BookingPage from "@/pages/BookingPage";
import AdminLogin from "@/pages/AdminLogin";
import AdminDashboard from "@/pages/AdminDashboard";
import SuperAdminPanel from "@/pages/SuperAdminPanel";
import GestioneSerate from "@/pages/GestioneSerate";
import CameraApp from "@/pages/CameraApp";
import QRCodeWindow from "@/components/QRCodeWindow";
import NoLicensePage from "@/pages/NoLicensePage";
import { Toaster } from "@/components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/book" replace />} />
          <Route path="/book" element={<BookingPage />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/serate" element={<GestioneSerate />} />
          <Route path="/super-admin" element={<SuperAdminPanel />} />
          <Route path="/camera/:serataId" element={<CameraApp />} />
          <Route path="/qrcode" element={<QRCodeWindow />} />
          <Route path="/no-license" element={<NoLicensePage />} />
          <Route path="*" element={<Navigate to="/book" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" />
    </div>
  );
}

export default App;