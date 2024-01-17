import "./app.scss";
import { ConfigProvider } from "antd";
import { Land } from "./pages/land/Land";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Serve } from "./pages/serve/Serve";
import { openSampleSite } from "./util/util";

export function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#001529",
          colorText: "#56514e",
          colorLink: "#001529",
        },
      }}
    >
      <BrowserRouter>
        <Routes>
          <Route index element={<Land />} />
          <Route path="land" element={<Land />} />
          <Route path="serve" element={<Serve />} />
          <Route path="sample" element={<>{openSampleSite()}</>} />
          <Route path="*" element={<Land />} />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}
