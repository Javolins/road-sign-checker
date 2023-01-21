import React from "react";
import { Routes, Route } from "react-router-dom";
import AppLayout from "./components/AppLayout";
import { paths, pathsHome } from "./paths"

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppLayout />}>
        {paths.map(({ path, pageComponent }) => <Route key={path} path={path} element={pageComponent} />)}
      </Route>
      <Route path="/" element={<AppLayout />}>
        {pathsHome.map(({ path, pageComponent }) => <Route key={path} path={path} element={pageComponent} />)}
      </Route>
      <Route path="*" element={<p>404 page</p>} />
    </Routes>

  );
}

export default App;
