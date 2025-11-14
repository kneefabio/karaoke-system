import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import BookingPage from "@/pages/BookingPage";
import AdminLogin from "@/pages/AdminLogin";
import AdminDashboard from "@/pages/AdminDashboard";
import SuperAdminPanel from "@/pages/SuperAdminPanel";
import GestioneSerate from "@/pages/GestioneSerate";
import CameraApp from "@/pages/CameraApp";
import { Toaster } from "@/components/ui/sonner";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<BookingPage />} />
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/serate" element={<GestioneSerate />} />
          <Route path="/super-admin" element={<SuperAdminPanel />} />
          <Route path="/camera/:serataId" element={<CameraApp />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-center" />
    </div>
  );
}

export default App;