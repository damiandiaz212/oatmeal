import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Admin } from "@/admin";
import "./index.css";
import { ConfigProvider, theme, App } from "antd";

const rootElement = document.querySelector('[data-js="root"]');

if (!rootElement) {
  throw new Error("Failed to find the root element");
}

const root = createRoot(rootElement);
root.render(
  <StrictMode>
    <ConfigProvider
      theme={{
        // 1. Use dark algorithm
        algorithm: theme.darkAlgorithm,

        // 2. Combine dark algorithm and compact algorithm
        // algorithm: [theme.darkAlgorithm, theme.compactAlgorithm],
      }}
    >
      <App>
        <Admin />
      </App>
    </ConfigProvider>
  </StrictMode>
);
