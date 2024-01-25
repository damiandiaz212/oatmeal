import "./app.scss";
import { ConfigProvider } from "antd";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import AdminLayout from "./pages/AdminLayout";

export function App() {
  return <AdminLayout />;
}
